from src.app.models import Sentence, CombinedSentences
from sklearn.metrics.pairwise import cosine_distances

from sentence_transformers import SentenceTransformer
from typing import List

import PyPDF2
import re


class PrepareForSemanticChunking:
    """Class to prepare the PDF file before semantic chunking"""

    def __init__(self, pdf: str, embedder_dir: str) -> None:
        """
        Args:
            pdf (str): The PDF file.
            embedder_dir (str): The directory path where the embedding model is located.
        """
        self.pdf = pdf
        self.embedder_dir = embedder_dir

    def _load_pdf(self, pattern: re.Pattern[str] = r"(?<=[.!?])\s+") -> List[Sentence]:
        """
        Loads a PDF from the specified path, splits its textinto sentences based on punctation
        marks and converts them into 'Sentence' objects.

        Args:
            pattern (re.Pattern[str]): A regex pattern to split sentences.

        Returns:
            List[Sentence]: A list of 'Sentence' objects.
        """
        reader = PyPDF2.PdfReader(self.pdf)

        full_text = ("").join(page.extract_text() for page in reader.pages)
        full_text = full_text.replace("\n", " ")
        splited_sentences = re.split(pattern=pattern, string=full_text)
        sentences = [Sentence(sen) for sen in splited_sentences]

        return sentences

    def _connect_sentences(
        self, sentences: List[Sentence], overlap: int = 1
    ) -> List[CombinedSentences]:
        """
        Connects sentences based on overlapping content.

        Args:
            sentences (List[Sentence]): A list of Sentence objects.
            overlap (int): The number of overlapping sentences to consider.

        Returns:
            List[CombinedSentences]: A list of CombinedSentences objects.
        """
        combined_sentences = []

        for i in range(len(sentences)):
            combined_sentence_text = ""

            for j in range(i - overlap, i):
                if j >= 0:
                    combined_sentence_text += f"{sentences[j].sentence} "

            combined_sentence_text += sentences[i].sentence

            for j in range(i + 1, i + 1 + overlap):
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
        self, pattern: re.Pattern[str] = r"(?<=[.!?])\s+", overlap: int = 1
    ) -> List[CombinedSentences]:
        """
        Prepares the document for recursive semantic chunking by:
        1. Loading the PDF and splitting it into sentences.
        2. Connecting sentences with overlap.
        3. Applying embeddings.
        4. Calculating cosine distances between embedding vectors.

        Args:
            pattern (re.Pattern[str]): A regex pattern to split sentences.
            overlap (int): The number of overlapping sentences to consider.

        Returns:
            List[CombinedSentences]: A list of 'CombinedSentences' objects with cosine distances
                computed between each pair of consecutive sentences.
        """
        sentences = self._load_pdf(pattern=pattern)
        combined_sentences = self._connect_sentences(
            sentences=sentences, overlap=overlap
        )
        combined_sentences = self._apply_embeddings(
            combined_sentences=combined_sentences
        )
        combined_sentences = self._compare_vectors(
            combined_sentences=combined_sentences
        )

        return combined_sentences
