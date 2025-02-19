from transformers import AutoModelForCausalLM, AutoTokenizer

from src.operations.database_operations import ChromaDBOperations
from src.utils import sentence_embedding


def retrieve_relevant_chunks(embedder_dir: str, query: str, top_k: int = 1) -> str:
    """
    Retrieves the top-k most relevant chunks from ChromaDB based on the query,
    and combines them into a single message string.

    Args:
        embedder_dir (str): Path to the directory storing embedding model.
        query (str): The query to be used for retrieving relevant chunks.
        top_k (int): The number of top chunks to retrieve

    Returns:
        str: A single string combining the top-k retrieved chunks
    """
    embedded_query = sentence_embedding(sentences=[query], embedder_dir=embedder_dir)

    chroma_oper = ChromaDBOperations()
    relevant_chunks = chroma_oper.retrieve_chunk(
        embedded_query=embedded_query[0], top_k=top_k
    )

    relevant_chunks = [item for sublist in relevant_chunks for item in sublist]
    relevant_chunks = "\n\n".join(
        [chunk.replace("\n", " ") for chunk in relevant_chunks]
    )
    return relevant_chunks


def get_response(query: str, context: str, transformer_dir: str, **kwargs) -> str:
    """
    Combines the query with the context and generates a response using transformer model.

    Args:
        query (str): The user's input query for which a response is needed.
        context (str): The relevant context of information that is used to answer the query.
        transformer_dir (str): The path to the transformer model directory for response generation.
        **kwargs: Additional parameters to customize the behavior of the transformer generation
    Returns:
        str: The generated response based on the input query and context
    """
    transformer = AutoModelForCausalLM.from_pretrained(transformer_dir)
    tokenizer = AutoTokenizer.from_pretrained(transformer_dir)

    input_text = f"""
    You are a helpful AI assistant. Answer the question strictly based on the provided context.
    If the answer is not in the context, say "I don't know."

    Context:
    {context}

    Question:
    {query}

    Answer:
    """
    input_ids = tokenizer(input_text, return_tensors="pt")

    outputs = transformer.generate(**input_ids, **kwargs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
