import os
import logging

from config import base_settings

from sentence_transformers import SentenceTransformer


def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def download_and_save_embedder() -> None:
    embedder_dir = base_settings.app.EMBEDDER_DIR
    ensure_dir(embedder_dir)

    model = SentenceTransformer("BAAI/bge-small-en")
    model.save(embedder_dir)

    logging.info(f"Model successfully saved to {embedder_dir}")


if __name__ == "__main__":
    download_and_save_embedder()
