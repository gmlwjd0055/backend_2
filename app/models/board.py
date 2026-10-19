from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base

class Board(Base):
    __tablename__ = "board"

    idx: Mapped[int] = mapped_column(primary_key=True) #중복x
    title: Mapped[str] = mapped_column()
    contents: Mapped[str] = mapped_column()
