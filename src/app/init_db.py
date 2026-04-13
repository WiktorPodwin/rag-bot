import logging

from app.core import init_db


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | [%(filename)s:%(lineno)d] | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Initializing the database tables.")
    init_db()
    logger.info("Database tables initialized successfully.")


if __name__ == "__main__":
    main()
