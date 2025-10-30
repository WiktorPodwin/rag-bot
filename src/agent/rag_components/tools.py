from operations.storages import ChromaDBOperations

from config import base_config
from langchain_core.tools import tool


@tool(parse_docstring=True)
def retriever(query: str) -> str:
    """
    Retrieves relevant informations from the database based on a user-provided query.

    Args:
        query (str): Natural language query string containing specific question related to the user's request.

    Returns:
        str: A text of relevant chunks retrieved from the database that match the query.
    """
    retriever = ChromaDBOperations(
        collection="documents", embedder_dir=base_config.EMBEDDER_DIR
    ).get_retriever(3)
    results = retriever.invoke(query)
    return "\n\n".join(res.page_content for res in results)


tools = [retriever]
tools_map = {tool.name: tool for tool in tools}
