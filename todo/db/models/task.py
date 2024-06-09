from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from todo.db.core import Base


class Task(Base):
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
