from src.operations.storages import ChromaDBOperations

from src.config import BaseConfig as config
from langchain_core.tools import tool

from typing import List


@tool(parse_docstring=True)
def retriever(query: str) -> List[str]:
    """
    Retrieves relevant informations from the database based on a user-provided query.

    Args:
        query (str): Natural language query string containing specific question related to the user's request.

    Returns:
        List[str]: A list of relevant chunks of text retrieved from the database that match the query.
    """
    retriever = ChromaDBOperations(
        collection="documents", embedder_dir=config.EMBEDDER_DIR
    ).get_retriever()
    results = retriever.invoke(query)
    return results


tools = [retriever]
tools_map = {tool.name: tool for tool in tools}
