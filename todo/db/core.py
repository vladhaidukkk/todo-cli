from itertools import islice
from typing import Optional

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from todo.config import dev_settings, settings

engine = create_engine(settings.db_url, echo=dev_settings.debug)
session_factory = sessionmaker(engine)

metadata = MetaData(
    naming_convention={
        "all_column_names": lambda constraint, table: "_".join(
            [column.name for column in constraint.columns.values()]  # type: ignore
        ),
        "ix": "ix_%(table_name)s_%(all_column_names)s",
        "uq": "uq_%(table_name)s_%(all_column_names)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(all_column_names)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
DeclarativeBase = declarative_base(metadata=metadata)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    __repr_limit__: Optional[int] = None
    __repr_ignore__: list[str] = []

    def __repr__(self) -> str:
        cols = [
            f"{col}={repr(getattr(self, col))}"
            for col in islice(self.__table__.columns.keys(), self.__repr_limit__)
            if col not in self.__repr_ignore__
        ]
        return f"<{self.__class__.__name__} {", ".join(cols)}>"
