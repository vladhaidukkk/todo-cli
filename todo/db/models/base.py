from itertools import islice
from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(table_name)s_%(column_0_N_name)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class Base(DeclarativeBase):
    metadata = metadata

    __repr_limit__: Optional[int] = None
    __repr_ignore__: tuple[str, ...] = ()

    def __repr__(self) -> str:
        cols = [
            f"{col}={getattr(self, col)!r}"
            for col in islice(self.__table__.columns.keys(), self.__repr_limit__)
            if col not in self.__repr_ignore__
        ]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
