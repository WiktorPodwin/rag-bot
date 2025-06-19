import logging

from src.app.core import init_db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Initializing the database tables.")
    init_db()
    logger.info("Database tables initialized successfully.")


if __name__ == "__main__":
    main()
