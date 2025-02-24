from src.core.config import settings
from sqlmodel import create_engine, Session

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def init_db() -> None:
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
