from pydantic import BaseModel, ConfigDict


class PaymentOrderRequest(BaseModel):
    course_id: int


class PaymentOrderResponse(BaseModel):
    payment_id: str
    course_id: int
    order_name: str
    amount_krw: int
    currency: str = "KRW"
    store_id: str
    channel_key: str


class PaymentConfirmRequest(BaseModel):
    payment_id: str


class PaymentStatusResponse(BaseModel):
    payment_id: str
    status: str
    course_id: int
