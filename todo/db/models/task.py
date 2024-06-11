from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todo.db.core import Base
from todo.db.types import created_at, intpk, updated_at

if TYPE_CHECKING:
    from .assertion import Assertion
    from .space import Space


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[intpk]
    title: Mapped[str]
    target_date: Mapped[Optional[date]]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    completed_at: Mapped[Optional[datetime]]
    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id"))

    space: Mapped["Space"] = relationship(back_populates="tasks")
    assertions: Mapped[list["Assertion"]] = relationship(back_populates="task")
