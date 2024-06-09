from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from todo.db.core import Base

if TYPE_CHECKING:
    from .checkbox import Checkbox


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    target_date: Mapped[Optional[date]]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(),
        onupdate=datetime.now(),
    )
    completed_at: Mapped[Optional[datetime]]

    checkboxes: Mapped[list["Checkbox"]] = relationship(back_populates="task")
