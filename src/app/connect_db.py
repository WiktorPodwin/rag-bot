import logging

from sqlmodel import select
from tenacity import retry, after_log, before_log, stop_after_attempt, wait_fixed

from app.core import get_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 2 * 60
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        session = get_session()
        session.exec(select(1))  # check if DB is awake
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing database service.")
    init()
    logger.info("Database service initialized successfully.")


if __name__ == "__main__":
    main()
