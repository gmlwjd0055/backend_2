from datetime import datetime, timezone
from uuid import uuid4

import jwt
import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import settings
from db.database import get_db
from models.course import Course
from models.payment import PaymentOrder
from schemas.payment import (
    PaymentConfirmRequest,
    PaymentOrderRequest,
    PaymentOrderResponse,
    PaymentStatusResponse,
)

router = APIRouter(prefix="/payments", tags=["payments"])


def authenticated_user(request: Request) -> str:
    token = request.cookies.get("EN_AT")
    if not token:
        raise HTTPException(status_code=401, detail="로그인 후 구매할 수 있습니다.")
    try:
        subject = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        ).get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="로그인이 만료되었습니다.")
    if not subject:
        raise HTTPException(status_code=401, detail="로그인이 만료되었습니다.")
    return subject


@router.post("/orders", response_model=PaymentOrderResponse)
def create_order(
    payload: PaymentOrderRequest,
    user_id: str = Depends(authenticated_user),
    db: Session = Depends(get_db),
):
    if not settings.PORTONE_STORE_ID or not settings.PORTONE_CHANNEL_KEY:
        raise HTTPException(status_code=503, detail="PortOne 결제 설정이 완료되지 않았습니다.")
    course = db.get(Course, payload.course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="강의를 찾을 수 없습니다.")
    payment_id = f"course-{course.id}-{uuid4().hex}"
    order = PaymentOrder(
        payment_id=payment_id,
        course_id=course.id,
        user_id=user_id,
        amount_krw=course.price_krw,
        status="PENDING",
    )
    db.add(order)
    db.commit()
    return PaymentOrderResponse(
        payment_id=payment_id,
        course_id=course.id,
        order_name=course.title,
        amount_krw=course.price_krw,
        store_id=settings.PORTONE_STORE_ID,
        channel_key=settings.PORTONE_CHANNEL_KEY,
    )


@router.post("/confirm", response_model=PaymentStatusResponse)
def confirm_payment(
    payload: PaymentConfirmRequest,
    user_id: str = Depends(authenticated_user),
    db: Session = Depends(get_db),
):
    order = db.scalar(
        select(PaymentOrder).where(
            PaymentOrder.payment_id == payload.payment_id,
            PaymentOrder.user_id == user_id,
        )
    )
    if order is None:
        raise HTTPException(status_code=404, detail="결제 주문을 찾을 수 없습니다.")
    if order.status == "PAID":
        return PaymentStatusResponse(
            payment_id=order.payment_id, status=order.status, course_id=order.course_id
        )
    if not settings.PORTONE_API_SECRET:
        raise HTTPException(status_code=503, detail="PortOne 서버 검증 설정이 완료되지 않았습니다.")

    try:
        response = requests.get(
            f"{settings.PORTONE_API_BASE_URL.rstrip('/')}/payments/{order.payment_id}",
            headers={"Authorization": f"PortOne {settings.PORTONE_API_SECRET}"},
            timeout=10,
        )
        response.raise_for_status()
        payment = response.json()
    except (requests.RequestException, ValueError):
        raise HTTPException(status_code=502, detail="PortOne 결제 정보를 확인하지 못했습니다.")

    amount = payment.get("amount") or {}
    if (
        payment.get("status") != "PAID"
        or amount.get("total") != order.amount_krw
        or payment.get("currency") != "KRW"
        or payment.get("id") != order.payment_id
    ):
        raise HTTPException(status_code=400, detail="결제 금액 또는 상태를 확인할 수 없습니다.")

    order.status = "PAID"
    order.paid_at = datetime.now(timezone.utc)
    db.commit()
    return PaymentStatusResponse(
        payment_id=order.payment_id, status=order.status, course_id=order.course_id
    )
