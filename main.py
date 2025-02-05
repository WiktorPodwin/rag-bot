import time

from src.pipelines import embed_pdfs_to_chromadb, retrieve_and_combine_chunks, get_response
from src.config import BaseConfig as config


if __name__ == "__main__":
    start = time.time()

    embed_pdfs_to_chromadb(config.EMBEDDER_DIR, config.PDF_DIR)

    query = "Who becomes a banker?"
    context = retrieve_and_combine_chunks(
        embedding_model_dir=config.EMBEDDER_DIR, query=query, top_k=2
    )

    response = get_response(query=query, 
                            context=context, 
                            transformer_dir=config.TRANSFORMER_DIR,
                            temperature=0.1,
                            do_sample=True,
                            max_new_tokens=70,
                            repetition_penalty=1.2,
                            top_p=0.9,
                            top_k=30
                            )
    print(response)
    print("\nComputing time:", time.time() - start)
