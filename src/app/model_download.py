import os
import logging

from config import base_settings

from sentence_transformers import SentenceTransformer


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | [%(filename)s:%(lineno)d] | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def download_and_save_embedder() -> None:
    embedder_dir = base_settings.app.EMBEDDER_DIR
    ensure_dir(embedder_dir)

    model = SentenceTransformer("BAAI/bge-small-en")
    model.save(embedder_dir)

    logger.info(f"Model successfully saved to {embedder_dir}")


if __name__ == "__main__":
    download_and_save_embedder()
