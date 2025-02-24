from src.core import init_blob_container

client = init_blob_container()


class BlobStorageOperations:

    def __init__(self) -> None:
        self.client = init_blob_container()


blob_list = client.list_blobs()
for blob in blob_list:
    print(blob)
