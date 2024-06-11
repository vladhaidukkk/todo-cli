from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from todo.db.core import Base
from todo.db.types import created_at, intpk, updated_at

if TYPE_CHECKING:
    from .task import Task


class Space(Base):
    __tablename__ = "spaces"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    tasks: Mapped[list["Task"]] = relationship(back_populates="space")
