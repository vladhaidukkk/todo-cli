from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from todo.config import settings

engine = create_engine(settings.db_url)
session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
