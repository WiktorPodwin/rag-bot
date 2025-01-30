import os
import logging

from attrs import define

logging.basicConfig(level=logging.INFO)

@define
class BaseConfig:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    DATA_DIR = os.path.join(BASE_DIR, "data")
    PDF_DIR = os.path.join(DATA_DIR, "pdfs")

    CHECKPOINTS = os.path.join(BASE_DIR, "checkpoints")
    EMBEDDER_DIR = os.path.join(CHECKPOINTS, "BAAI/bge-small-en")
    TRANSFORMER_DIR = os.path.join(CHECKPOINTS, "google/gemma-2b")

    