from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todo.db.types import intpk

from .base import Base

if TYPE_CHECKING:
    from .space import Space


class SpaceHistoryRecord(Base):
    __tablename__ = "spaces_history"

    id: Mapped[intpk]
    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id", ondelete="CASCADE"))
    active_status: Mapped[bool]
    changed_at: Mapped[datetime]

    space: Mapped["Space"] = relationship(back_populates="history_records")
