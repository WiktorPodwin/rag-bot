from upload_pdfs.handle_data.pictures import HandlePictures
from upload_pdfs.handle_data.tables import HandleTables

from upload_pdfs.utils import from_bytes_to_document_stream
from upload_pdfs.uploader import PdfLoader

from io import BytesIO


class PreprocessPDF:

    def __init__(self, pdf: BytesIO, pdf_name: str = "") -> None:
        loader = PdfLoader()
        formated_pdf = from_bytes_to_document_stream(pdf=pdf, pdf_name=pdf_name)
        self.document = loader.load_pdf(formated_pdf)
        self.doc_items = list(self.document.iterate_items())
        self.table_oper = HandleTables()
        self.picture_oper = HandlePictures()

    def _check_if_next_element_for_current_is_caption(self, actual_id: int) -> bool:
        next_id = actual_id + 1

        if next_id < len(self.doc_items):
            return self.doc_items[next_id][0].label == "caption"

        return False

    def _check_if_neccessary_to_add_new_lines(self, actual_id: int) -> bool:
        next_id = actual_id + 1

        if next_id < len(self.doc_items):
            if self.doc_items[actual_id][0].label == "text" and self.doc_items[next_id][
                0
            ].label in [
                "list_item",
                "picture",
                "table",
            ]:
                return True
        return False

    def preprocess(self) -> str:
        caption_check = False
        markdown_text = ""
        text_from_element = ""

        for i, (element, _) in enumerate(self.doc_items):
            label = element.label
            add_new_line = self._check_if_neccessary_to_add_new_lines(i)

            if label == "picture":
                text_from_element = (
                    f"`{self.picture_oper.handle_picture_data(image=element)}`\n\n"
                )
                caption_check = self._check_if_next_element_for_current_is_caption(i)

            elif label == "table":
                text_from_element = (
                    f"`{self.table_oper.handle_tabular_data(table=element)}`\n\n"
                )
                caption_check = self._check_if_next_element_for_current_is_caption(i)

            elif label == "caption":
                text_from_element = f"\n***{element.text}***\n\n{text_from_element}"
                caption_check = False

            elif label == "section_header":
                text_from_element = f"\n\n## {element.text}\n"

            elif label == "list_item":
                text_from_element = f"- {element.text}\n"

            else:
                text_from_element += element.text

            if add_new_line:
                text_from_element = f"{text_from_element}\n\n"

            if not caption_check:
                markdown_text += text_from_element
                text_from_element = ""

        return markdown_text
