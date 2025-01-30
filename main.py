import time

from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer

from src.operations import ChromaDBOperations, list_files
from src.config import BaseConfig as config


if __name__ == "__main__":
    start = time.time()


    chroma_oper = ChromaDBOperations(config.TRANSFORMER_DIR)

    pdfs = list_files(config.PDF_DIR, full_path=True)
    
    all_chunk_ids = []
    for pdf in pdfs:
        chunks_ids = chroma_oper.add_document(pdf_path=pdf, return_ids=True)
        all_chunk_ids.extend(chunks_ids)
    
    chroma_oper.remove_chunks(ids_to_keep=all_chunk_ids)

    query = "When Monopoly has been invented?"
    results = chroma_oper.retrive_chunk(query, 3)
    results = ("\n\n".join([result.replace("\n", " ") for result in results]))
    print(results)

    





    # context = "\n".join(retrieved_docs)
    # input_text = f"""You are a helpful AI assistant. Answer the question strictly based on the provided context.
    # If the answer is not in the context, say "I don't know."

    # Context:
    # {context}

    # Question:
    # {query}

    # Answer:
    # """

    # transformer = AutoModelForCausalLM.from_pretrained(transformer_dir)

    # tokenizer = AutoTokenizer.from_pretrained(transformer_dir)

    # input_ids = tokenizer(input_text, return_tensors="pt")

    # outputs = transformer.generate(
    #     **input_ids,
    #     max_new_tokens=100,
    #     temperature=0.3,
    #     top_p=0.9,
    #     do_sample=True,
    #     repetition_penalty=1.2
    # )
    # print(tokenizer.decode(outputs[0], skip_special_tokens=True))

    print("\nComputing time:", time.time() - start)