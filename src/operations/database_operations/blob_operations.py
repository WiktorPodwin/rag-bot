from src.core import init_blob_container

from azure.storage.blob import BlobProperties

from io import BytesIO
from typing import List


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
