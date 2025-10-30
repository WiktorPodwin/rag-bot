from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    AcceleratorDevice,
    AcceleratorOptions,
    TableFormerMode,
)
from docling.datamodel.base_models import InputFormat
from docling_core.types.io import DocumentStream
from docling_core.types.doc import DocItemLabel

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types import DoclingDocument
from config import base_config

from docling_ocr_onnxtr import OnnxtrOcrOptions
import logging


class PdfLoader:

    def __init__(
        self,
        number_of_threads: int = base_config.NUMBER_OF_THREADS,
        image_resolution_scale: float = base_config.IMAGE_RESOLUTION_SCALE,
    ) -> None:
        self.textual_labels = {
            DocItemLabel.TEXT,
            DocItemLabel.TITLE,
            DocItemLabel.SECTION_HEADER,
            DocItemLabel.FOOTNOTE,
            DocItemLabel.LIST_ITEM,
            DocItemLabel.PARAGRAPH,
            DocItemLabel.REFERENCE,
        }

        ocr_options = OnnxtrOcrOptions()
        pipeline_options = PdfPipelineOptions(
            do_ocr=True,
            accelerator_options=AcceleratorOptions(
                num_threads=number_of_threads, device=AcceleratorDevice.CPU
            ),
            do_table_structure=True,
            allow_external_plugins=True,
        )

        pipeline_options.table_structure_options.mode = TableFormerMode.FAST
        pipeline_options.table_structure_options.do_cell_matching = False
        pipeline_options.do_ocr = False
        pipeline_options.ocr_options = ocr_options
        pipeline_options.images_scale = image_resolution_scale
        pipeline_options.generate_picture_images = True

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def load_pdf(self, pdf: DocumentStream) -> DoclingDocument:
        try:
            extracted_pdf = self.converter.convert(pdf)
        except Exception as e:
            logging.error(
                f"Error while loading the pdf: {pdf.name}. Error message: {e}"
            )
            raise e

        return extracted_pdf.document
