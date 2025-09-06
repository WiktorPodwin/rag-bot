from langchain_text_splitters.markdown import MarkdownHeaderTextSplitter

from typing import List


class MarkdownSplitter:
    def __init__(self, chunk_min_length: int = 300) -> None:
        self.chunk_min_length = chunk_min_length
        self.headers_to_split_on = [
            ("#", "Header"),
            ("##", "Section 1"),
            ("###", "Section 2"),
        ]

    def apply_markdown_chunking(self, markdown_text: str) -> List[str]:
        if len(markdown_text) / 2 < self.chunk_min_length:
            return [markdown_text]

        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on
        )
        splitted_text = splitter.split_text(markdown_text)

        results = []
        for chunk in splitted_text:
            chunk_content = chunk.page_content

            headers_content = [val for val in chunk.metadata.values()]
            if headers_content:
                chunk_content = ".\n".join(headers_content) + ".\n" + chunk_content

            results.append(chunk_content)

        return results
