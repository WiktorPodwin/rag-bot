import chromadb
import hashlib
import logging

from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from chromadb.errors import InvalidArgumentError


class ChromaDBOperations:

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8800,
        collection: str = "documents",
    ) -> None:
        """
        Initiate parameters

        Args:
            host (str): Type of host
            port (int): Port number
            collection (str): Name of the collection to store documents inside ChromaDB
        """
        self.collection_name = collection
        self.chroma_client = chromadb.HttpClient(host=host, port=port)
        self.collection = self.chroma_client.get_or_create_collection(name=collection)

    def remove_collection(self) -> None:
        """
        Deletes the whole collection
        """
        try:
            self.chroma_client.delete_collection(self.collection_name)
            logging.info(f'Successfully deleted collection: "{self.collection_name}"')
        except InvalidArgumentError:
            logging.warning(f'Collection "{self.collection_name}" does not exist')

    def remove_chunks(
        self,
        ids_to_delete: List[str] | None = None,
        ids_to_keep: List[str] | None = None,
    ) -> None:
        """
        Deletes chunks from the collection

        Args:
            ids_to_delete (List[str] | None): List of chunk IDs to delete. If neither 'ids_to_delete' or 'ids_to_keep' is provided, all chunks will be removed.
            ids_to_keep (List[str] | None): List of chunk IDs to keep. If provided, all chunks not in this list will be deleted.
        """
        try:
            if not ids_to_delete or ids_to_keep:
                all_docs = self.collection.get(ids=None)
                ids_to_delete = all_docs["ids"]

                if ids_to_keep:
                    ids_to_delete = [
                        id for id in ids_to_delete if id not in ids_to_keep
                    ]
                    if ids_to_delete == []:
                        logging.info(f"No chunks were removed")
                        return

            self.collection.delete(ids=ids_to_delete)
            logging.info(f"Successfully removed {len(ids_to_delete)} chunks")
        except ValueError:
            logging.warning(f'Collection "{self.collection_name}" is already empty')

    def _split_into_chunks(
        self, pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 200
    ) -> List[str]:
        """
        Uploads the PDF file and splits the text into smaller chunks for storage and retrieval

        Args:
            pdf_path (str): The PDF containing text to be splitted into chunks
            chunk_size (int) Size of each chunk
            chunk_overlap (int): Number of overlapping characters between chunks

        Returns:
            List[str]: A list of text chunks that are derived from the input text
        """
        loader = PyPDFLoader(pdf_path)
        docs = loader.load_and_split()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        chunks = []
        for doc in docs:
            chunks.extend((text_splitter.split_text(doc.page_content)))
        return chunks

    def add_document(
        self, embedding_model_dir: str, pdf_path: str, return_ids: bool = False
    ) -> List[str] | None:
        """
        Add a document to ChromaDB after opening the PDF file, spliting text into chunks and creating embeddings.

        Args:
            embedding_model_dir (str): Path to the directory storing embedding model.
            pdf_path (str): The PDF containing text to be splitted into chunks.
            return ids (bool): If the function should return applied chunks ID.

        Returns:
            List[str] | None: List of chunks id if return_ids is set to True, else None
        """
        embedder = SentenceTransformer(embedding_model_dir)
        chunks = self._split_into_chunks(pdf_path)

        new_ids = []
        for chunk in chunks:
            doc_id = hashlib.sha256(chunk.encode()).hexdigest()
            if return_ids:
                new_ids.append(doc_id)

            existing = self.collection.get(ids=[doc_id])
            if not existing["metadatas"]:
                embedding = embedder.encode(chunk).tolist()
                self.collection.add(
                    ids=[doc_id], embeddings=[embedding], metadatas=[{"text": chunk}]
                )
                logging.info(f"Successfully added chunk: {doc_id}")
        if return_ids:
            return new_ids

    def retrieve_chunk(
        self, embedding_model_dir: str, query: str, top_k: int = 1
    ) -> List[str | None]:
        """
        Retrieves the top-k most relevant chunks from ChromaDB based on the query.

        Args:
            embedding_model_dir (str): Path to the directory storing embedding model.
            query (str): The query to be used for retrieving relevant chunks.
            top_k (int): The number of top chunks to retrieve

        Returns:
            List[str | None]: A list of strings representing the top-k relevant chunks of text.
        """
        embedder = SentenceTransformer(embedding_model_dir)
        query_embedding = embedder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )
        return (
            [doc["text"] for doc in results["metadatas"][0]]
            if results.get("metadatas")
            else []
        )
