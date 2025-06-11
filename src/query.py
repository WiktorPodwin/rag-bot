import time

from config import BaseConfig as config
from pipelines import retrieve_relevant_chunks


if __name__ == "__main__":
    start = time.time()

    query = "Did Lizzy earn some money from the Monopoly?"
    chunks = retrieve_relevant_chunks(config.EMBEDDER_DIR, query=query, top_k=3)
    print(chunks)

    # response = get_response(query=query,
    #                         context=context,
    #                         transformer_dir=config.TRANSFORMER_DIR,
    #                         temperature=0.1,
    #                         do_sample=True,
    #                         max_new_tokens=70,
    #                         repetition_penalty=1.2,
    #                         top_p=0.9,
    #                         top_k=30
    #                         )
    # print(response)

    print("\n\nComputing time: ", time.time() - start)
