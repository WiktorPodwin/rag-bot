from re import Pattern

from src.operations.chunk_operations import (
    PrepareForSemanticChunking,
    ReduceChunkSize,
    EnhanceChunkSize,
    extract_chunks,
    visualize_chunks,
)


def recursive_semantic_chunking(
    pdf_path: str,
    embedder_dir: str,
    pattern: Pattern[str] = r"(?<=[.!?])\s+",
    overlap: int = 1,
    percentage: int = 98,
    max_size: int = 1000,
    min_size: int = 300,
):
    """
    Performs recursive semantic chunking on a PDF document.

    This function process a PDF file by:
    1. Splitting the text into sentences.
    2. Connecting sentences with overlapping content.
    3. Applying embeddings to combined sentences.
    4. Calculating cosine diistances between wentence embeddings.
    5. Creating chunks by splitting at high cosine distance points.
    6. Reducing chunk sizes by splitting in local minima.
    7. Enhancing chunk sizes by merging smaller chunks.
    8. Extracting the final chunk context.

    Args:
        pdf_path (str): The path to the PDF file.
        embedder_dir (str): The directory path where the embedding model is located.
        pattern (Pattern[str]): A regex pattern to split sentences.
        overlap (int): The number of overlapping sentences to consider.
        percentage (int): The percentile to calculate.
        max_size (int): The maximum size for a chunk.
        min_size (int): The minimum size for a chunk.

    Returns:
        List[str]: A list of extracted text chunks.
    """
    prepare_for_chunking = PrepareForSemanticChunking(
        pdf_path=pdf_path, embedder_dir=embedder_dir
    )
    combined_sentences = prepare_for_chunking.prepare_for_recursive_semantic_chunking(
        pattern=pattern, overlap=overlap
    )

    reduce_chunk_size = ReduceChunkSize()
    combined_sentences, chunks = reduce_chunk_size.reduce_size(
        combined_sentences=combined_sentences, percentage=percentage, max_size=max_size
    )

    enhance_chunk_size = EnhanceChunkSize()
    combined_sentences, chunks = enhance_chunk_size.enhance_size(
        combined_sentences=combined_sentences, chunks=chunks, min_size=min_size
    )

    visualize_chunks(
        combined_sentences=combined_sentences, save_path="data/graphs/chunks.png"
    )

    extracted_chunks = extract_chunks(combined_sentences=combined_sentences)

    return extracted_chunks
