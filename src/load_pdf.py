import time

from pipelines import handle_pdfs
from config import BaseConfig as config


if __name__ == "__main__":
    start = time.time()

    handle_pdfs(config.EMBEDDER_DIR)

    print("\nComputing time:", time.time() - start)
