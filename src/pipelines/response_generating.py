from transformers import AutoModelForCausalLM, AutoTokenizer


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

    outputs = transformer.generate(
        **input_ids,
        **kwargs
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
