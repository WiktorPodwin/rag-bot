from src.upload_pdfs.data_extraction.text.chunking.utils import (
    extract_chunks,
    visualize_chunks,
)

from src.upload_pdfs.data_extraction.text.chunking import (
    PrepareForSemanticChunking,
    ReduceChunkSize,
    EnhanceChunkSize,
)

from src.upload_pdfs.data_extraction.text.utils import sentence_embedding

from typing import List, Tuple
from re import Pattern


def recursive_semantic_chunking(
    pdf: str,
    embedder_dir: str,
    pattern: Pattern[str] = r"(?<=[.!?])\s+",
    overlap: int = 1,
    percentage: int = 98,
    max_size: int = 1000,
    min_size: int = 300,
    save_path: str | None = "data/graphs/chunks.png",
) -> Tuple[List[str], List[List[float]]]:
    """
    Performs recursive semantic chunking on a PDF document.

    This function processes a PDF file by:
    1. Splitting the text into sentences.
    2. Connecting sentences with overlapping content.
    3. Applying embeddings to combined sentences.
    4. Calculating cosine distances between wentence embeddings.
    5. Creating chunks by splitting at high cosine distance points.
    6. Reducing chunk sizes by splitting at local minima.
    7. Enhancing chunk sizes by merging smaller chunks.
    8. Extracting the final chunk context.

    Args:
        pdf (str): The PDF file.
        embedder_dir (str): The directory path where the embedding model is located.
        pattern (Pattern[str]): A regex pattern to split sentences.
        overlap (int): The number of overlapping sentences to consider.
        percentage (int): The percentile used for chunk size reduction.
        max_size (int): The maximum allowable size for a chunk.
        min_size (int): The minimum allowable size for a chunk.
        save_path (str | None): Path for the visualization of the chunking process.
            If is None, visualization will not be saved.

    Returns:
        Tuple[List[str], List[List[float]]]: A list of extracted text chunks and
            a list of their cooresponding embeddings.
    """
    prepare_for_chunking = PrepareForSemanticChunking(
        pdf=pdf, embedder_dir=embedder_dir
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

    if save_path:
        visualize_chunks(combined_sentences=combined_sentences, save_path=save_path)

    extracted_chunks = extract_chunks(combined_sentences=combined_sentences)
    embeddings = sentence_embedding(
        sentences=extracted_chunks, embedder_dir=embedder_dir
    )

    return extracted_chunks, embeddings
