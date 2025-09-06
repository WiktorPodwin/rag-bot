from pydantic_settings import BaseSettings
from pydantic import Field, computed_field

import logging
import os

logging.basicConfig(level=logging.INFO)


class BaseConfig(BaseSettings):
    IMAGE_RESOLUTION_SCALE: float = Field(
        2.5, description="Resolution scale in extracted images from PDF."
    )
    NUMBER_OF_THREADS: int | None = Field(
        description="Number of threads available in current device.",
        default_factory=os.cpu_count,
    )

    MIN_CHUNK_LENGTH: int = Field(
        300,
        description="Approximated minimum chunk length during recursive semantic chunking.",
    )
    MAX_CHUNK_LENGTH: int = Field(
        1000,
        description="Approximated maximum chunk length during recursive semantic chunking.",
    )
    PERCENTILE_THRESHOLD: int = Field(
        98,
        description="The percentile where the cosine distance is the highest, and the chunk has to be cut off during recursive semantic chunking",
    )

    @computed_field
    @property
    def BASE_DIR(self) -> str:
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

    @computed_field
    @property
    def EMBEDDER_DIR(self) -> str:
        return os.path.join(self.BASE_DIR, "checkpoints/BAAI/bge-small-en")

    @computed_field
    @property
    def DATA_DIR(self) -> str:
        return os.path.join(self.BASE_DIR, "data")


base_config = BaseConfig()
