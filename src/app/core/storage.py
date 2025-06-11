from azure.storage.blob import BlobServiceClient, ContainerClient

from app.core.config import settings


def init_blob_container() -> ContainerClient:
    """
    Estabilished and returns a connection to an Azure Blob Storage container.

    Returns:
        ContainerClient: A client instance connected to the specified container.
    """
    blob_service_client = BlobServiceClient.from_connection_string(
        conn_str=settings.AZURE_STORAGE_CONNECTION_STRING
    )
    return blob_service_client.get_container_client(container=settings.CONTAINER_NAME)
