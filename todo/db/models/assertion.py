from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todo.db.core import Base
from todo.db.types import created_at, intpk, updated_at

if TYPE_CHECKING:
    from .task import Task


class Assertion(Base):
    __tablename__ = "assertions"

    id: Mapped[intpk]
    title: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    completed_at: Mapped[Optional[datetime]]
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))

    task: Mapped["Task"] = relationship(back_populates="assertions")
