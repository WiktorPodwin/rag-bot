from src.agent.rag_components.llm import llm

from docling_core.types.io import DocumentStream

from langchain_core.messages import HumanMessage

from typing import List, Dict
from io import BytesIO


def from_bytes_to_document_stream(pdf: BytesIO, pdf_name: str) -> DocumentStream:
    return DocumentStream(name=pdf_name, stream=pdf)


def summarize_object(message_content: List[Dict[str, str]] | str) -> str:
    msg = HumanMessage(content=message_content)
    response = llm.invoke([msg])
    return "\n" + response.content
