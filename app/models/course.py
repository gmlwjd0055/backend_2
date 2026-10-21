from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class Course(Base):
    __tablename__ = "course"
    __table_args__ = (
        CheckConstraint("price_krw >= 0", name="ck_course_price_nonnegative"),
        CheckConstraint(
            "duration_minutes >= 0", name="ck_course_duration_nonnegative"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    thumbnail_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    instructor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price_krw: Mapped[int] = mapped_column(nullable=False)
    level: Mapped[str] = mapped_column(String(50), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(nullable=False)
