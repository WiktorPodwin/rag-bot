from typing import List

from sentence_transformers import SentenceTransformer


def sentence_embedding(sentences: List[str], embedder_dir: str) -> List[List[float]]:
    """
    Generates embeddings for a list of strings using SentenceTransformer model.

    Args:
        sentences (List[str]): A list of strings to embed.
        embedder_dir (str): The directory path where the embedding model is located.

    Returns:
        List[List[float]]: A list of embeddings, where each embedding is a list of floats.
    """
    embedder = SentenceTransformer(embedder_dir)
    embeddings = []

    for sentence in sentences:
        embeddings.append(embedder.encode(sentence).tolist())

    return embeddings
