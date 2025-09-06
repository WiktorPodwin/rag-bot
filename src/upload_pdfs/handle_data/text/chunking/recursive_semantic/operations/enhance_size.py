from src.upload_pdfs.handle_data.text.chunking.recursive_semantic.operations.utils import (
    reset_chunk_index,
)

from src.app.models import CombinedSentences, Chunk

from typing import List, Tuple


class EnhanceChunkSize:
    """Class for enhancing chunk size."""

    def _handle_boundary_chunks(
        self,
        combined_sentences: List[CombinedSentences],
        chunks: List[Chunk],
        min_size: int = 300,
    ) -> Tuple[List[CombinedSentences], List[Chunk]]:
        """
        Merges boundary chunks with their neighbors if their size is to small.

        Args:
            combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.
            chunks (List[Chunk]): A list of 'Chunk' objects.
            max_size (int): The minimum size for a chunk.

        Returns:
            Tuple[List[CombinedSentences], List[Chunk]]: The updatet list of 'CombinedSentences' with
                updated chunks indices, along with un updated list of 'Chunk' objects after merging.
        """
        while True:
            if not chunks or len(chunks) <= 1:
                break

            boundary_indexes = [0, -1]
            merged = False

            for id in boundary_indexes:
                if chunks[id].is_too_small:
                    if id == 0:
                        neighbour = 1
                    else:
                        neighbour = -2

                    future_chunk = chunks[neighbour].chunk_index
                    for x in range(len(combined_sentences)):
                        if combined_sentences[x].chunk_index == chunks[id].chunk_index:
                            combined_sentences[x].chunk_index = future_chunk

                    chunks[neighbour].size += chunks[id].size
                    if id == -1:
                        chunks[neighbour].cosine_distance = chunks[
                            neighbour
                        ].cosine_distance

                    if chunks[neighbour].size >= min_size:
                        chunks[neighbour].is_too_small = False

                    chunks.pop(id)
                    merged = True
                    break
            if not merged:
                break

        return combined_sentences, chunks

    def _handle_interior_chunks(
        self,
        combined_sentences: List[CombinedSentences],
        chunks: List[Chunk],
        min_size: int = 300,
    ) -> Tuple[List[CombinedSentences], List[Chunk]]:
        """
        Merges interior chunks with their neighbors based on cosine distance. The neighbor with the lower
        cosine distance will be connected to the current chunk.

        Args:
            combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.
            chunks (List[Chunk]): A list of 'Chunk' objects.
            max_size (int): The minimum size for a chunk.

        Returns:
            Tuple[List[CombinedSentences], List[Chunk]]: The updatet list of 'CombinedSentences' with
                updated chunks indices, along with un updated list of 'Chunk' objects after merging.
        """
        i = 0
        while i < len(chunks):

            if chunks[i].is_too_small:
                if chunks[i - 1].cosine_distance <= chunks[i + 1].cosine_distance:
                    neighbour = -1
                else:
                    neighbour = 1

                merged_id = i + neighbour

                for x in range(len(combined_sentences)):
                    if combined_sentences[x].chunk_index == chunks[i].chunk_index:
                        combined_sentences[x].chunk_index = chunks[
                            merged_id
                        ].chunk_index

                chunks[merged_id].size += chunks[i].size

                if chunks[merged_id].size >= min_size:
                    chunks[merged_id].is_too_small = False

                if neighbour == -1:
                    chunks[merged_id].cosine_distance = chunks[i].cosine_distance
                chunks.pop(i)

            else:
                i += 1

        return combined_sentences, chunks

    def enhance_size(
        self,
        combined_sentences: List[CombinedSentences],
        chunks: List[Chunk],
        min_size: int = 300,
    ) -> Tuple[List[CombinedSentences], List[Chunk]]:
        """
        Checks each chunk's size. If the size is too small, it will connect the chunk with its neighbor.

        Args:
            combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.
            chunks (List[Chunk]): A list of 'Chunk' objects.
            min_size (int): The minimum size for a chunk.

        Returns:
            Tuple[List[CombinedSentences], List[Chunk]]: The updatet list of 'CombinedSentences' with
                updated chunks indices, along with un updated list of 'Chunk' objects after merging.
        """
        distances = {}

        for sen in combined_sentences:
            distances[sen.chunk_index] = sen.cosine_distance

        for chunk in chunks:
            chunk.is_too_small = chunk.size < min_size
            chunk.cosine_distance = distances[chunk.chunk_index]

        combined_sentences, chunks = self._handle_boundary_chunks(
            combined_sentences=combined_sentences, chunks=chunks, min_size=min_size
        )
        combined_sentences, chunks = self._handle_interior_chunks(
            combined_sentences=combined_sentences, chunks=chunks, min_size=min_size
        )
        combined_sentences, chunks = reset_chunk_index(
            combined_sentences=combined_sentences, chunks=chunks
        )
        return combined_sentences, chunks
