import numpy as np
import matplotlib.pyplot as plt

from typing import List

from src.app.models import CombinedSentences


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
