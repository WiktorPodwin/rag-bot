from src.app.models import CombinedSentences, Chunk

from typing import List, Tuple


def reset_chunk_index(
    combined_sentences: List[CombinedSentences], chunks: List[Chunk] = None
) -> List[CombinedSentences] | Tuple[List[CombinedSentences], List[Chunk]]:
    """
    Reassigns chunk indexes sequentially, without changing the sentence order.

    Args:
        combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.
        chunks (List[Chunk]): A list of 'Chunk' objects.

    Returns:
        List[CombinedSentences]: The updated list with chunk indices reassigned in a sequential order.
        Tuple[List[CombinedSentences], List[Chunk]]: If 'chunks' is provided, returns the updated sentence
        list along with the updated chunk list.
    """
    equivalents = {}
    new_chunk_index = 1

    for sen in combined_sentences:
        old_index = sen.chunk_index
        if old_index not in equivalents:
            equivalents[old_index] = new_chunk_index
            new_chunk_index += 1
        sen.chunk_index = equivalents[old_index]

    if chunks:
        for chunk in chunks:
            chunk.chunk_index = equivalents[chunk.chunk_index]

        chunks.sort(key=lambda chunk: chunk.chunk_index)

        return combined_sentences, chunks

    return combined_sentences


def extract_chunks(combined_sentences: List[CombinedSentences]) -> List[str]:
    """
    Extracts sentences from a list of 'CombinedSentences' objects and groups them into chunks
    based on their chunk index.

    Args:
        combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.

    Returns:
        List[str]: A list of chunks, where each chunk is a string of concatenated sentences
        sharing the same chunk index.
    """
    extracted_chunks = []
    chunk = ""
    current_chunk = combined_sentences[0].chunk_index

    for i in range(len(combined_sentences)):
        if current_chunk != combined_sentences[i].chunk_index:
            if len(chunk) > 0:
                extracted_chunks.append(chunk.strip())
            chunk = ""

        chunk += " " + combined_sentences[i].sentence
        current_chunk = combined_sentences[i].chunk_index

    if len(chunk) > 0:
        extracted_chunks.append(chunk.strip())

    return extracted_chunks
