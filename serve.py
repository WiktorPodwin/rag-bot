from src.agent.graphs import agent

from langserve import add_routes
from fastapi import FastAPI

import uvicorn

app = FastAPI(debug=True, version="1.0")

add_routes(app, agent)

# if __name__ == "__main__":
#     uvicorn.run("serve:app", host="127.0.0.1", port=8000)
