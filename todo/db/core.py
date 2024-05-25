from itertools import islice

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from todo.config import settings

engine = create_engine(settings.db_url)
session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    __repr_limit__: int | None = None
    __repr_ignore__: list[str] = []

    def __repr__(self) -> str:
        cols = [
            f"{col}={getattr(self, col)}"
            for col in islice(self.__table__.columns.keys(), self.__repr_limit__)
            if col not in self.__repr_ignore__
        ]
        return f"<{self.__class__.__name__} {", ".join(cols)}>"
