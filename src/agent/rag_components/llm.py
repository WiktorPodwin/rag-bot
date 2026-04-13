from config import base_settings
from langchain_openai.chat_models.base import ChatOpenAI


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=base_settings.llm.OPENAI_API_KEY.get_secret_value(),
    temperature=0,
    max_retries=2,
    max_tokens=3000,
)
