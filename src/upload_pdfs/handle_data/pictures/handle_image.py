from src.upload_pdfs.utils import summarize_object
from docling_core.types.doc import PictureItem


class HandlePictures:

    def _check_if_picture_not_too_small(self, width: int, height: int) -> bool:
        area = width * height
        if area < 20000:
            return True
        return False

    def _summarize_picture(self, image_url: str) -> str:
        content = [
            {
                "type": "text",
                "text": "Describe the content of this image in 1-2 sentences.",
            },
            {
                "type": "image_url",
                "image_url": {"url": image_url},
            },
        ]
        # return summarize_object(content)
        return "Summary of some image"

    def handle_picture_data(self, image: PictureItem) -> str:
        too_small = self._check_if_picture_not_too_small(
            image.image.size.width, image.image.size.height
        )

        if too_small:
            return ""
        return self._summarize_picture(str(image.image.uri))
