from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Sentence:
    """
    Represents an individual sentence with an unique ID.

    Attributes:
        id (int): A unique identifier assigned automatically.
        sentence (str): The sentence text.
        chunk_index (Optional[int]): The ID of the chunk it belongs to.
    """

    index: int = field(init=False)
    sentence: str = ""
    chunk_index: Optional[int] = None

    _id_counter: int = 0

    def __post_init__(self):
        """Automatically assign a unique ID to each new Sentence instance."""
        self.__class__._id_counter += 1
        self.index = self.__class__._id_counter

    def __repr__(self):
        """Custom string representation to hide _id_counter."""
        return f"Sentence(index={self.index}, sentence={repr(self.sentence)}, chunk_index={self.chunk_index})"


@dataclass
class CombinedSentences(Sentence):
    """
    Represents a sentence combined with neighboring sentences for context.

    Inherits from Sentence and adds:
        combined_sentence (str): The sentence combined with its neighbors.
        embeddings (List[float]): A list of float values representing sentence embeddings.
        cosine_distance (Optional[float]): The cosine distance with the next sentence.
        is_above_percentile (bool): If the cosine distance is above the specified percentile threshold.
    """

    combined_sentence: str = ""
    embeddings: List[float] = field(default_factory=list)
    cosine_distance: Optional[float] = None
    is_above_percentile: bool = None

    _id_counter: int = 0

    def __post_init__(self):
        """Ensure each CombinedSentences gets its own unique index."""
        super().__post_init__()

    def __repr__(self):
        """Custom string representation to hide _id_counter."""
        return f"CombinedSentences(index={self.index}, sentence={repr(self.sentence)}, combined_sentence={repr(self.combined_sentence)}, embeddings={self.embeddings}, cosine_distance={self.cosine_distance}, chunk_index={self.chunk_index}, above_threshold={self.above_threshold})"


@dataclass
class Chunk:
    """
    Represents a chunk of sentences grouped together.

    Attributes:
        chunk_index (int): A unique identifier assigned automatically.
        size (int): The total size of the chunk.
        cosine_distance (Optional[float]): The cosine distance for merging.
        is_too_big (Optional[bool]): Whether the chunk exceeds the upper size threshold.
        is_too_small (Optional[bool]): Whether the chunk is below the minimum size threshold.
    """

    chunk_index: int = 0
    size: int = 0
    cosine_distance: Optional[float] = None
    is_too_big: Optional[bool] = None
    is_too_small: Optional[bool] = None
