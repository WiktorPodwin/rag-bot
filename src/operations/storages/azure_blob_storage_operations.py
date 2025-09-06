from src.app.core import init_blob_container

from azure.storage.blob import BlobProperties

from io import BytesIO
from typing import List

import hashlib


class BlobStorageOperations:
    """Provides methods for interacting with Azure Blob Storage"""

    def __init__(self) -> None:
        """
        Initializes a connection to the blob container.
        """
        self.client = init_blob_container()

    def list_file_metadatas(self) -> List[BlobProperties]:
        """
        Retrieves metadata for all blobs in the container.

        Returns:
            List[BlobProperties]: A list of blob metadata objects.
        """
        blob_list = self.client.list_blobs()
        return list(blob_list)

    def download_blob(self, blob_name: str) -> BytesIO:
        """
        Downloades a blob from the container and returns it as a byte stream.

        Args:
            blob_name (str): The name of the blob to download.

        Returns:
            BytesIO: A byte stream containing the blob data.
        """
        blob_client = self.client.get_blob_client(blob=blob_name)
        pdf = blob_client.download_blob()
        pdf = pdf.readall()
        pdf = BytesIO(pdf)
        return pdf

    def delete_blob(self, blob_name: str) -> None:
        """
        Deletes a blob from the container, including any snapshots if they exist.

        Args:
            blob_name (str): The name of the blob to delete.
        """
        self.client.delete_blob(blob=blob_name, delete_snapshots="include")

    def delete_all_blobs(self) -> None:
        """
        Deletes all blobs from the container, including any snapshots if they exist.
        """
        blob_metadatas = self.list_file_metadatas()
        for blob in blob_metadatas:
            self.delete_blob(blob.name)

    def add_blob(
        self, blob_name: str, blob_content: bytes, check_if_present_in_db: bool = True
    ) -> str:
        """
        Add a new blob to the container

        Args:
            blob_name (str): The name of the blob.
            blob_content (bytes): The content of the blob.
            check_if_present_in_db (bool): If it have to be ensured that in the database there is no file with the same name or content.

        Returns:
            str: A message with the status of the operation.
        """

        content_md5 = hashlib.md5(blob_content).hexdigest()

        if check_if_present_in_db:
            from src.operations.storages import DBOperations
            from src.app.connect_db import get_session

            db_oper = DBOperations(get_session())
            present_file = db_oper.get_file_metadata(content_md5=content_md5)

            if present_file:
                return (
                    f"In database already exists a file {present_file.name} with the same content, so your file will not be added. "
                    "To add your current file, you have to delete the old one first."
                )

            present_file = db_oper.get_file_metadata(name=blob_name)
            if present_file:
                return (
                    f"In database already exists a file {present_file.name} with the same name, so your file will not be added. "
                    "To add your current file, you have to delete the old one first."
                )

        blob_client = self.client.get_blob_client(blob_name)
        blob_client.upload_blob(BytesIO(blob_content), overwrite=True)

        return f"Successfully added new PDF to the storage with the name: {blob_name}"
