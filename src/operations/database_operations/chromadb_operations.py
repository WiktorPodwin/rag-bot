import chromadb
import logging
import hashlib

from typing import List, Tuple
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
        content_md5,
    ) -> None:
        """
        Adds already prepared chunks to ChromaDB.

        Args:
            embeddings (List[str]): A list of embeddings applied on chunks.
            chunks (List[str]): A list of extracted text chunks.
            content_md5 (str): The MD5 hash of the context ot the file to store in chunk metadata.
        """
        chunk_ids = [self._generate_chunk_id(chunk) for chunk in chunks]
        metadatas = [{"content_md5": content_md5} for _ in chunks]

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

    def remove_collection(self) -> None:
        """
        Deletes the whole collection.
        """
        try:
            self.chroma_client.delete_collection(self.collection_name)
            logging.info(f'Successfully deleted collection: "{self.collection_name}"')
        except InvalidArgumentError:
            logging.warning(f'Collection "{self.collection_name}" does not exist')

    def remove_chunks(self, ids_to_delete: List[str] = None) -> None:
        """
        Deletes chunks from the collection

        Args:
            ids_to_delete (List[str]): List of chunk IDs to delete.
                If nothing provided, it will delete all of the chunks from the collection.
        """
        try:
            if ids_to_delete is None:
                all_chunks = self.collection.get(include=["metadatas"])
                ids_to_delete = all_chunks.get("ids", [])

            self.collection.delete(ids=ids_to_delete)
            logging.info(f"Successfully removed {len(ids_to_delete)} chunks")

        except ValueError:
            logging.warning(
                f'No chunk IDs found in collection "{self.collection_name}". Nothing to delete.'
            )

    def find_md5_to_delete(self, md5_to_keep: List[str]) -> Tuple[List[str], List[str]]:
        """
        Identifies outdated chunks in the collection by compairing their metadata's content_md5
        against a provided list of hashes to retain.
        Args:
            md5_to_keep List[str]: A list of MD5 hashes to retain.

        Returns:
            Tuple[List[str], List[str]]:
             - A list of chunk IDs to delete from the collection.
             - A list of MD5 hashes to remove from the database.
        """
        all_chunks = self.collection.get(include=["metadatas"])

        all_md5s = [
            metadata.get("content_md5") for metadata in all_chunks.get("metadatas", [])
        ]

        ids_to_delete = [
            all_chunks.get("ids")[i]
            for i, content_md5 in enumerate(all_md5s)
            if content_md5 not in md5_to_keep
        ]

        md5_to_delete = [
            content_md5
            for content_md5 in all_md5s
            if content_md5 and content_md5 not in md5_to_keep
        ]

        if not ids_to_delete and not md5_to_delete:
            logging.info("All chunks are up to date. No deletions needed.")
        else:
            logging.info(f"Found {len(ids_to_delete)} outdated chunks to delete.")
        return ids_to_delete, md5_to_delete
