from src.app.models import CombinedSentences, Chunk

from sentence_transformers import SentenceTransformer
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


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

    if not current_chunk:
        return [sen.combined_sentence for sen in combined_sentences]

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


def visualize_chunks(
    combined_sentences: List[CombinedSentences],
    save_path: str,
    percentile: float = None,
) -> None:
    """
    Visualizes the cosine distance between consecutive sentences and highlights chunks areas.

    Args:
        combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects containing
            'cosine_distance' values and chunk identifiers.
        save_path (str): The file path to save the generated plot.
        percentile (float): A cosine distance percentile to display as a horizontal red line.
    """
    x_array = range(1, len(combined_sentences) + 1)
    distances = [
        combined_sentences[i].cosine_distance for i in range(len(combined_sentences))
    ]
    max_y = np.max(distances)

    plt.plot(x_array, distances, color="blue", label="Cosine Distances")
    if percentile:
        plt.axhline(percentile, color="red", linestyle="--", label="Percentile")

    colors = ["blue", "green", "red", "pink", "yellow", "brown", "purple"]

    start_index = 0
    current_chunk = combined_sentences[0].chunk_index
    chunk_count = 0

    for x in range(len(combined_sentences)):
        if (
            x == len(combined_sentences) - 1
            or combined_sentences[x + 1].chunk_index != current_chunk
        ):

            plt.axvspan(
                start_index,
                x + 1,
                facecolor=colors[chunk_count % len(colors)],
                alpha=0.25,
            )
            plt.text(
                x=np.average([start_index, x + 1]),
                y=max_y * 0.8,
                s=f"Chunk #{chunk_count}",
                horizontalalignment="center",
                rotation="vertical",
            )
            if x < len(combined_sentences) - 1:
                current_chunk = combined_sentences[x + 1].chunk_index

            start_index = x + 1
            chunk_count += 1

    plt.title("Cosine distances of sentences")
    plt.xlabel("Combined sentences index")
    plt.ylabel("Cosine distance")
    plt.legend(loc="lower right")
    plt.xlim(0, len(combined_sentences))
    plt.ylim(0, max_y * 1.15)
    plt.savefig(save_path)
    plt.close()


def sentences_embedding(sentences: List[str], embedder_dir: str) -> List[List[float]]:
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
