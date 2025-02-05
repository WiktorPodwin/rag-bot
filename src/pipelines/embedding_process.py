from src.operations import ChromaDBOperations, list_files


def embed_pdfs_to_chromadb(embedding_model_dir: str, pdf_dir: str) -> None:
    """
    Process PDF by generating embeddings ans storing them in ChromaDB.

    This function:
    1. Loads PDFs from the specified directory.
    2. Splits each PDF into chunks.
    3. Deletes outdated embeddings.
    4. Applies new embeddings and save them in ChromaDB.

    Args:
        embedding_model_dir (str): Path to the directory containing the embedding model.
        pdf_dir (str): Path to the directory containing PDF files.
    """
    chroma_oper = ChromaDBOperations()
    pdfs = list_files(pdf_dir, full_path=True)

    all_chunk_ids = []
    for pdf in pdfs:
        chunks_ids = chroma_oper.add_document(
            embedding_model_dir=embedding_model_dir, pdf_path=pdf, return_ids=True
        )
        all_chunk_ids.extend(chunks_ids)

    chroma_oper.remove_chunks(ids_to_keep=all_chunk_ids)


def retrieve_and_combine_chunks(
    embedding_model_dir: str, query: str, top_k: int = 1
) -> str:
    """
    Retrieves the top-k most relevant chunks from ChromaDB based on the query,
    and combines them into a single message string.

    Args:
        embedding_model_dir (str): Path to the directory storing embedding model.
        query (str): The query to be used for retrieving relevant chunks.
        top_k (int): The number of top chunks to retrieve

    Returns:
        str: A single string combining the top-k retrieved chunks
    """
    chroma_oper = ChromaDBOperations()
    results = chroma_oper.retrieve_chunk(
        embedding_model_dir=embedding_model_dir, query=query, top_k=top_k
    )
    results = "\n".join([result.replace("\n", " ") for result in results])
    return results
