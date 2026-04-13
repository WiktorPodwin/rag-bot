from config import base_settings
from sqlmodel import create_engine, Session

engine = create_engine(base_settings.db.SQLALCHEMY_DATABASE_URI.get_secret_value())


def init_db() -> None:
    """
    Initializes the database and creates all tables defined by SQLModel.
    """
    from sqlmodel import SQLModel
    import app.models  # noqa F401

    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Creates and returns a new database session.
    """
    return Session(engine)
