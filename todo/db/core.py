from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todo.config import dev_settings, settings

engine = create_engine(settings.db_url, echo=dev_settings.debug)
session_factory = sessionmaker(engine)
