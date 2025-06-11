from src.operations.database_operations import (
    ChromaDBOperations,
    BlobStorageOperations,
    DBOperations,
)
from src.operations import recursive_semantic_chunking
from src.app.core import get_session

from typing import Any


def _handle_pdf(pdf: str, content_md5: str, embedder_dir: str, **kwargs: Any) -> None:
    """
    Performs recursive semantic chunking on a PDF document and adds embedded chunks to the database.

    Args:
        pdf (str): The PDF file.
        content_md5 (str): The MD5 hash of the context ot the file.
        embedder_dir (str): The directory path where the embedding model is located.
        **kwargs (Any): Additional parameters for recursive semantic chunking.
    """
    chunks, embeddings = recursive_semantic_chunking(
        pdf=pdf, embedder_dir=embedder_dir, **kwargs
    )

    chroma_oper = ChromaDBOperations()
    chroma_oper.add_chunks(
        embeddings=embeddings, chunks=chunks, content_md5=content_md5
    )


def handle_pdfs(embedder_dir: str, **chunking_params: Any) -> None:
    """
    Handles processing PDFs, performing semantic chunking and removing outdated chunks.

    Args:
        embedder_dir (str): The directory path where the embedding model is located.
        **chunking_params (Any): Additional chunking parameters passed to '_handle_pdf'
    """
    blob_oper = BlobStorageOperations()
    blob_list = blob_oper.list_file_metadatas()

    session = get_session()
    db_oper = DBOperations(session=session)
    md5_to_keep = []

    for blob in blob_list:
        content_md5 = blob.content_settings.content_md5.hex()

        if not db_oper.get_file_metadata(content_md5):
            pdf = blob_oper.download_blob(blob.name)
            _handle_pdf(
                pdf=pdf,
                content_md5=content_md5,
                embedder_dir=embedder_dir,
                **chunking_params
            )

            db_oper.create_file_metadata(
                name=blob.name,
                content_md5=content_md5,
                last_modified=blob.last_modified,
            )

        md5_to_keep.append(content_md5)

    chroma_oper = ChromaDBOperations()
    ids_to_delete, md5_to_delete = chroma_oper.find_md5_to_delete(
        md5_to_keep=md5_to_keep
    )

    if ids_to_delete:
        chroma_oper.remove_chunks(ids_to_delete)

    if md5_to_delete:
        for md5 in md5_to_delete:
            db_oper.delete_file_metadata(content_md5=md5)
