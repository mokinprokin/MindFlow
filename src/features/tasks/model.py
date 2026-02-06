from sqlalchemy import Boolean, text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base

class TasksModel(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    time_from: Mapped[str]
    time_to:Mapped[str]
    task: Mapped[str]
    priority: Mapped[str]
    is_done: Mapped[bool | None] = mapped_column(
        Boolean, default=False, server_default=text("0")
    )