
from sqlalchemy import (
    create_engine,
    URL,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from todo_app.config import settings

class Base(DeclarativeBase):
    pass

connection_uri = URL.create(
    settings.db_engine,
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_host,
    database=settings.db_database_name,
)

engine = create_engine(connection_uri, echo=True)

SessionLocal = sessionmaker(
    engine
)
