from upload_pdfs.handle_data.text.chunking.recursive_semantic.operations.utils import (
    extract_chunks,
    sentences_embedding,
    visualize_chunks,
)

from upload_pdfs.handle_data.text.chunking.recursive_semantic.operations import (
    PrepareForSemanticChunking,
    ReduceChunkSize,
    EnhanceChunkSize,
)

from typing import List, Tuple


def recursive_semantic_chunking(
    chunks_before_processing: List[str],
    embedder_dir: str,
    percentage: int = 98,
    min_size: int = 300,
    max_size: int = 1000,
    save_path: str | None = "data/graphs/chunks.png",
) -> Tuple[List[str], List[List[float]]]:
    """
    Performs recursive semantic chunking on a list of already preprocessed chunks.

    This function processes each chunk by:
    1. Splitting the text into sentences.
    2. Connecting sentences with overlapping content.
    3. Applying embeddings to combined sentences.
    4. Calculating cosine distances between wentence embeddings.
    5. Creating chunks by splitting at high cosine distance points.
    6. Reducing chunk sizes by splitting at local minima.
    7. Enhancing chunk sizes by merging smaller chunks.
    8. Extracting the final chunk context.

    Args:
        chunks_before_processing (List[str]): The list of chunks for further processing.
        embedder_dir (str): The directory path where the embedding model is located.
        percentage (int): The percentile used for chunk size reduction.
        min_size (int): The minimum allowable size for a chunk.
        max_size (int): The maximum allowable size for a chunk.
        save_path (str | None): Path for the visualization of the chunking process.
            If is None, visualization will not be saved.

    Returns:
        Tuple[List[str], List[List[float]]]: A list of extracted text chunks and
            a list of their cooresponding embeddings.
    """
    prepare_for_chunking = PrepareForSemanticChunking(embedder_dir=embedder_dir)
    reduce_chunk_size = ReduceChunkSize()
    enhance_chunk_size = EnhanceChunkSize()

    final_chunks: List[str] = []
    final_embeddings: List[List[float]] = []

    for chunk in chunks_before_processing:
        combined_sentences = (
            prepare_for_chunking.prepare_for_recursive_semantic_chunking(text=chunk)
        )

        if len(combined_sentences) > 3:
            combined_sentences, chunks = reduce_chunk_size.reduce_size(
                combined_sentences=combined_sentences,
                percentage=percentage,
                max_size=max_size,
            )

            combined_sentences, chunks = enhance_chunk_size.enhance_size(
                combined_sentences=combined_sentences, chunks=chunks, min_size=min_size
            )

        # if save_path:
        #     visualize_chunks(combined_sentences=combined_sentences, save_path=save_path)

        extracted_chunks = extract_chunks(combined_sentences=combined_sentences)
        embeddings = sentences_embedding(
            sentences=extracted_chunks, embedder_dir=embedder_dir
        )

    final_chunks.extend(extracted_chunks)
    final_embeddings.extend(embeddings)

    return final_chunks, final_embeddings
