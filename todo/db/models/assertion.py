from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from todo.db.core import Base

if TYPE_CHECKING:
    from .task import Task


class Assertion(Base):
    __tablename__ = "assertions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(),
        onupdate=datetime.now(),
    )
    completed_at: Mapped[Optional[datetime]]
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))

    task: Mapped["Task"] = relationship(back_populates="assertions")
