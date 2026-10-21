from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class PaymentOrder(Base):
    __tablename__ = "payment_order"
    __table_args__ = (
        CheckConstraint("amount_krw >= 0", name="ck_payment_order_amount_nonnegative"),
        UniqueConstraint("payment_id", name="uq_payment_order_payment_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    amount_krw: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDING")
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )
    paid_at: Mapped[datetime | None] = mapped_column(nullable=True)
