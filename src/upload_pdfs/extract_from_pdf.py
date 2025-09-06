from src.upload_pdfs.handle_data.text.chunking.markdown import MarkdownSplitter

from src.upload_pdfs.handle_data.text.chunking.recursive_semantic import (
    recursive_semantic_chunking,
)
from src.operations.storages import (
    ChromaDBOperations,
    BlobStorageOperations,
    DBOperations,
)

from src.upload_pdfs.handle_data import PreprocessPDF
from src.app.core import get_session

from src.config import base_config

from io import BytesIO


def _handle_pdf(pdf: BytesIO, content_md5: str, embedder_dir: str) -> None:
    """
    Performs recursive semantic chunking on a PDF document and adds embedded chunks to the database.

    Args:
        pdf (BytesIO): The PDF file stored in bytes.
        content_md5 (str): The MD5 hash of the context ot the file.
        embedder_dir (str): The directory path where the embedding model is located.
    """
    preprocess_pdf = PreprocessPDF(pdf=pdf)
    markdown_text = preprocess_pdf.preprocess()

    markdown_splitter = MarkdownSplitter(base_config.MIN_CHUNK_LENGTH)
    chunks = markdown_splitter.apply_markdown_chunking(markdown_text=markdown_text)

    chunks, embeddings = recursive_semantic_chunking(
        chunks_before_processing=chunks,
        embedder_dir=embedder_dir,
        percentage=base_config.PERCENTILE_THRESHOLD,
        min_size=base_config.MIN_CHUNK_LENGTH,
        max_size=base_config.MAX_CHUNK_LENGTH,
    )

    chroma_oper = ChromaDBOperations()
    chroma_oper.add_chunks(
        embeddings=embeddings, chunks=chunks, content_md5=content_md5
    )


def handle_pdfs() -> None:
    """
    Handles processing PDFs, performing semantic chunking and removing outdated chunks.
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
                pdf=pdf, content_md5=content_md5, embedder_dir=base_config.EMBEDDER_DIR
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
