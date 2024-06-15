from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from todo.db.types import created_at, intpk, updated_at

from .base import Base

if TYPE_CHECKING:
    from .space_history_record import SpaceHistoryRecord
    from .task import Task


class Space(Base):
    __tablename__ = "spaces"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    active: Mapped[bool] = mapped_column(server_default=expression.false())
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    disabled_at: Mapped[Optional[datetime]]

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="space", passive_deletes=True
    )
    history_records: Mapped[list["SpaceHistoryRecord"]] = relationship(
        back_populates="space", passive_deletes=True
    )
