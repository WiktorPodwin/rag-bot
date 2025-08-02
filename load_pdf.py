from src.upload_pdfs.data_extraction import handle_pdfs

from src.config import BaseConfig as config

import time

if __name__ == "__main__":
    start = time.time()

    handle_pdfs(config.EMBEDDER_DIR)

    print("\nComputing time:", time.time() - start)
