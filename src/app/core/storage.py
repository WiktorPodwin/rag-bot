from azure.storage.blob import BlobServiceClient, ContainerClient

from config import base_settings


def init_blob_container() -> ContainerClient:
    """
    Estabilished and returns a connection to an Azure Blob Storage container.

    Returns:
        ContainerClient: A client instance connected to the specified container.
    """
    blob_service_client = BlobServiceClient.from_connection_string(
        conn_str=base_settings.azure.AZURE_STORAGE_CONNECTION_STRING.get_secret_value()
    )
    return blob_service_client.get_container_client(
        container=base_settings.azure.CONTAINER_NAME
    )
