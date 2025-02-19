from src.operations import recursive_semantic_chunking
from src.operations.database_operations import ChromaDBOperations

from re import Pattern


def handle_pdf(
    pdf_path: str,
    embedder_dir: str,
    pattern: Pattern[str] = r"(?<=[.!?])\s+",
    overlap: int = 1,
    percentage: int = 98,
    max_size: int = 1000,
    min_size: int = 300,
) -> None:
    """
    Performs recursive semantic chunking on a PDF document and adds embedded chunks to the database.

    Args:
        pdf_path (str): The path to the PDF file.
        embedder_dir (str): The directory path where the embedding model is located.
        pattern (Pattern[str]): A regex pattern to split sentences.
        overlap (int): The number of overlapping sentences to consider.
        percentage (int): The percentile used for chunk size reduction.
        max_size (int): The maximum allowable size for a chunk.
        min_size (int): The minimum allowable size for a chunk.
    """
    chunks, embeddings = recursive_semantic_chunking(
        pdf_path=pdf_path,
        embedder_dir=embedder_dir,
        pattern=pattern,
        overlap=overlap,
        percentage=percentage,
        max_size=max_size,
        min_size=min_size,
    )

    chroma_oper = ChromaDBOperations()
    chroma_oper.add_chunks(embeddings=embeddings, chunks=chunks)
