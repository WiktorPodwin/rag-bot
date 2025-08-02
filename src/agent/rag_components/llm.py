import os
from dotenv import load_dotenv

from langchain_openai.chat_models.base import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1,
    max_retries=2,
    max_tokens=3000,
)
