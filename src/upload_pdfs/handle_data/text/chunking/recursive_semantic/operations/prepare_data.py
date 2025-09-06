from src.app.models import Sentence, CombinedSentences
from sklearn.metrics.pairwise import cosine_distances

from sentence_transformers import SentenceTransformer
from typing import List

import re


class PrepareForSemanticChunking:
    """
    Class to prepare a text before semantic chunking

    Attrubutes:
        pattern (re.Pattern[str]): A regex pattern to split sentences.
        overlap (int): The number of overlapping sentences to consider.
    """

    def __init__(self, embedder_dir: str) -> None:
        """
        Args:
            embedder_dir (str): The directory path where the embedding model is located.

        """
        self.embedder_dir = embedder_dir
        self.pattern: re.Pattern[str] = r"(?<=[.!?])\s+"
        self.overlap: int = 1

    def _preprocess_data(self, text: str) -> List[Sentence]:
        """
        Splits the text into sentences based on punctation marks and converts them into 'Sentence' objects.

        Args:
            text (str): Chunk of text already splitted by markdown splitter.

        Returns:
            List[Sentence]: A list of 'Sentence' objects.
        """
        text = text.replace("\n", " ")
        splited_sentences = re.split(pattern=self.pattern, string=text)
        sentences = [Sentence(sen) for sen in splited_sentences]
        return sentences

    def _connect_sentences(self, sentences: List[Sentence]) -> List[CombinedSentences]:
        """
        Connects sentences based on overlapping content.

        Args:
            sentences (List[Sentence]): A list of Sentence objects.
        Returns:
            List[CombinedSentences]: A list of CombinedSentences objects.
        """
        combined_sentences = []

        for i in range(len(sentences)):
            combined_sentence_text = ""

            for j in range(i - self.overlap, i):
                if j >= 0:
                    combined_sentence_text += f"{sentences[j].sentence} "

            combined_sentence_text += sentences[i].sentence

            for j in range(i + 1, i + 1 + self.overlap):
                if j < len(sentences):
                    combined_sentence_text += f" {sentences[j].sentence}"

            combined_sentences.append(
                CombinedSentences(
                    sentence=sentences[i].sentence,
                    combined_sentence=combined_sentence_text,
                    chunk_index=sentences[i].chunk_index,
                )
            )

        return combined_sentences

    def _apply_embeddings(
        self,
        combined_sentences: List[CombinedSentences],
    ) -> List[CombinedSentences]:
        """
        Applies embedding on the text of combined sentences.

        Args:
            combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.

        Returns:
            List[CombinedSentences]: A list of 'CombinedSentences' objects with
                embeddings src.applied to each combined sentence.
        """
        embedder = SentenceTransformer(self.embedder_dir)

        for i in range(len(combined_sentences)):
            combined_sentences[i].embeddings = embedder.encode(
                combined_sentences[i].combined_sentence
            ).tolist()

        return combined_sentences

    def _compare_vectors(
        self,
        combined_sentences: List[CombinedSentences],
    ) -> List[CombinedSentences]:
        """
        Compares the cosine distance between consecutive sentence embeddings.

        Args:
            combined_sentences (List[CombinedSentences]): A list of 'CombinedSentences' objects.

        Returns:
            List[CombinedSentences]: A list of 'CombinedSentences' objects with cosine distances
                computed between each pair of consecutive sentences.
        """
        for i in range(len(combined_sentences) - 1):
            current_embedding = combined_sentences[i].embeddings
            next_embedding = combined_sentences[i + 1].embeddings
            distance = cosine_distances([current_embedding], [next_embedding])[0][0]

            combined_sentences[i].cosine_distance = distance

        combined_sentences[-1].cosine_distance = distance
        return combined_sentences

    def prepare_for_recursive_semantic_chunking(
        self, text: str
    ) -> List[CombinedSentences]:
        """
        Prepares the document for recursive semantic chunking by:
        1. Splitting the chunk of text into sentences.
        2. Connecting sentences with overlap.
        3. Applying embeddings.
        4. Calculating cosine distances between embedding vectors.

        Args:
            text (str): Chunk of text already splitted by markdown splitter.

        Returns:
            List[CombinedSentences]: A list of 'CombinedSentences' objects with cosine distances
                computed between each pair of consecutive sentences.
        """
        sentences = self._preprocess_data(text=text)
        if len(sentences) <= 3:
            return [
                CombinedSentences(
                    combined_sentence=" ".join(sen.sentence for sen in sentences)
                )
            ]

        combined_sentences = self._connect_sentences(sentences=sentences)
        combined_sentences = self._apply_embeddings(
            combined_sentences=combined_sentences
        )
        combined_sentences = self._compare_vectors(
            combined_sentences=combined_sentences
        )

        return combined_sentences
