from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from todo.config import config

engine = create_engine(config.db_url)
session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
