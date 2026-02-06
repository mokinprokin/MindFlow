import datetime

from typing import List
from sqlalchemy import func, Float, JSON, text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base


class WordsModel(Base):
    __tablename__ = "words"
    id: Mapped[int] = mapped_column(primary_key=True)
    in_english: Mapped[str]
    in_russian: Mapped[List[str]] = mapped_column(JSON) 
    next_review: Mapped[datetime.date] = mapped_column(
        default=datetime.date.today,
        server_default=text("DATE('now')"),
        index=True
    )
    interval: Mapped[int] = mapped_column(default=0)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    repetition_count: Mapped[int] = mapped_column(default=0)
    last_review: Mapped[datetime.datetime | None] = mapped_column(default=None)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
