from src.datatypes import CombinedSentences, Chunk
from src.operations.chunk_operations.utils import reset_chunk_index

from typing import List, Tuple

import numpy as np


class ReduceChunkSize:
    """Class for reducing chunks sizes"""

    def _calculate_percentile(
        self, combined_sentences: List[CombinedSentences], percentage: int = 98
    ) -> float:
        """
        Calculates the specified percentile of cosine distances

        Args:
            combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.
            percentage (int): The percentile to calculate.

        Returns:
            float: The q-th percentile of the cosine distances.
        """
        if not combined_sentences:
            return None

        distances = [sen.cosine_distance for sen in combined_sentences]

        threshold = np.percentile(distances, percentage)
        return threshold

    def _sentences_above_threshold(
        self, combined_sentences: List[CombinedSentences], threshold: float
    ) -> List[CombinedSentences]:
        """
        Marks sentences with a cosine distance above the given threshold as 'is_above_percentile'.

        Args:
            combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.
            threshold (float): The cosine distance threshold for marking sentences.

        Returns:
            List[CombinedSentences]: A list of 'CombinedSentences' objects with 'is_above_percentile' marked.
        """
        check_list = []

        for i, sentence in enumerate(combined_sentences):
            sentence.is_above_percentile = (
                True
                if sentence.cosine_distance >= threshold
                and i < len(combined_sentences) - 1
                else False
            )
            check_list.append(sentence.is_above_percentile)

        if True not in check_list:
            return self._sentences_above_threshold(
                combined_sentences=combined_sentences, threshold=threshold * 0.99
            )

        return combined_sentences

    def _assign_chunks(
        self,
        combined_sentences: List[CombinedSentences],
        max_size: int,
        chunk_index: int = None,
    ) -> Tuple[List[CombinedSentences], List[Chunk]]:
        """
        Assign chunk indices to the sentences, and creates chunks based on the 'is_above_percentile' condition.

        Args:
            combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.
            max_size (int): The maximum size for a chunk.
            chunk_index (int): The starting index for chunks.

        Returns:
            Tuple[List[CombinedSentences], List[Chunk]]: The updatet list of 'CombinedSentences' with
                assigned chunk indices, along with a list of 'Chunk' objects representing the created chunks.
        """
        chunk_size = 0
        chunks = []

        if not chunk_index:
            chunk_index = 0

        for i, sen in enumerate(combined_sentences):
            combined_sentences[i].chunk_index = chunk_index
            chunk_size += len(sen.sentence)

            if sen.is_above_percentile or i == len(combined_sentences) - 1:
                chunks.append(
                    Chunk(
                        chunk_index=chunk_index,
                        size=chunk_size,
                        is_too_big=True if chunk_size > max_size else False,
                    )
                )
                chunk_size = 0
                chunk_index += 1

        return combined_sentences, chunks

    def reduce_size(
        self,
        combined_sentences=List[CombinedSentences],
        percentage: int = 98,
        max_size: int = 1000,
    ) -> Tuple[List[CombinedSentences], List[Chunk]]:
        """
        Splits the chunks if their size is too large.

        Args:
            combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.
            percentage (int): The percentile to calculate.
            max_size (int): The maximum size for a chunk.

        Returns:
            Tuple[List[CombinedSentences], List[Chunk]]: The updatet list of 'CombinedSentences' with
                updated chunks indices, along with un updated list of 'Chunk' objects containing the new chunks.
        """
        threshold = self._calculate_percentile(
            combined_sentences=combined_sentences, percentage=percentage
        )
        combined_sentences = self._sentences_above_threshold(
            combined_sentences=combined_sentences, threshold=threshold
        )
        combined_sentences, chunks = self._assign_chunks(
            combined_sentences=combined_sentences, max_size=max_size
        )

        sub_sentences = []
        i = 0
        while i < len(chunks):
            if chunks[i].is_too_big:
                sub_sentences = []
                sub_indexes = []

                for j in range(len(combined_sentences)):
                    if combined_sentences[j].chunk_index == chunks[i].chunk_index:
                        sub_sentences.append(combined_sentences[j])
                        sub_indexes.append(j)

                threshold = self._calculate_percentile(
                    combined_sentences=sub_sentences, percentage=percentage
                )
                sub_sentences = self._sentences_above_threshold(
                    combined_sentences=sub_sentences, threshold=threshold
                )
                last_index = np.max([ch.chunk_index for ch in chunks])
                sub_sentences, sub_chunks = self._assign_chunks(
                    combined_sentences=sub_sentences,
                    max_size=max_size,
                    chunk_index=last_index + 1,
                )
                chunks.pop(i)
                chunks.extend(sub_chunks)

                for x in range(len(sub_indexes)):
                    combined_sentences.pop(sub_indexes[x])
                    combined_sentences.insert(sub_indexes[x], sub_sentences[x])

            else:
                i += 1

        combined_sentences, chunks = reset_chunk_index(
            combined_sentences=combined_sentences, chunks=chunks
        )

        return combined_sentences, chunks
