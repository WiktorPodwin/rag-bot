import chromadb
import logging
import uuid
import hashlib

from typing import List
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
        Deletes the whole collection.
        """
        try:
            self.chroma_client.delete_collection(self.collection_name)
            logging.info(f'Successfully deleted collection: "{self.collection_name}"')
        except InvalidArgumentError:
            logging.warning(f'Collection "{self.collection_name}" does not exist')

    def _generate_chunk_id(self, chunk: str) -> str:
        """
        Generates an unique ID for a text chunk using a MD5 hash.

        Args:
            chunk (str): The text chunk to hash.

        Returns:
            str: The hexadecimal MD5 hash of the chunk.
        """
        return hashlib.md5(chunk.encode()).hexdigest()

    def add_chunks(
        self,
        embeddings: List[List[float]],
        chunks: List[str],
        metadatas: List[dict] = None,
    ) -> None:
        """
        Adds already prepared chunks to ChromaDB.

        Args:
            embeddings (List[str]): A list of embeddings applied on chunks.
            chunks (List[str]): A list of extracted text chunks.
            metadatas (List[dict]): A list of additional informations for each chunk.
        """
        chunk_ids = [self._generate_chunk_id(chunk) for chunk in chunks]

        self.collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        logging.info("Successfully added chunks to the database.")

    def retrieve_chunk(
        self, embedded_query: List[float], top_k: int = 1
    ) -> List[str | None]:
        """
        Retrieves the top-k most relevant chunks from ChromaDB based on the query.

        Args:
            embedded_query (List[float]): Query after ebedding.
            top_k (int): The number of top chunks to retrieve.

        Returns:
            List[str | None]: A list of strings representing the top-k relevant chunks of text.
        """
        results = self.collection.query(
            query_embeddings=[embedded_query], n_results=top_k
        )

        return results.get("documents", [])

    def remove_chunks(self, ids_to_delete: List[str] = None) -> None:
        """
        Deletes chunks from the collection

        Args:
            ids_to_delete (List[str]): List of chunk IDs to delete.
                If nothing provided, it will delete all of the chunks from the collection.
        """
        try:
            if ids_to_delete is None:
                all_chunks = self.collection.get(include=["ids"])
                ids_to_delete = all_chunks.get("ids", [])

            if ids_to_delete:
                self.collection.delete(ids=ids_to_delete)
                logging.info(f"Successfully removed {len(ids_to_delete)} chunks")

        except ValueError:
            logging.warning(f'Collection "{self.collection_name}" is already empty')
