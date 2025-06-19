from src.app.core.config import settings
from sqlmodel import create_engine, Session

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def init_db() -> None:
    """
    Initializes the database and creates all tables defined by SQLModel.
    """
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Creates and returns a new database session.
    """
    print(settings.POSTGRES_USER)
    print(settings.POSTGRES_DB)
    print(settings.POSTGRES_PASSWORD)
    print(settings.POSTGRES_HOST)
    return Session(engine)
