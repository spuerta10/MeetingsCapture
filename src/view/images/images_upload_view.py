from typing import ClassVar

from streamlit import file_uploader
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.view.base_view import BaseView


class ImagesUploadView(BaseView):
    ALLOWED_IMAGE_FORMATS: ClassVar[list[str]] = [".jpg", ".jpeg", ".png"]

    # @override
    def render(self) -> None | list[UploadedFile]:
        uploaded_images: list[UploadedFile] = file_uploader(
            label="Sube tus imágenes aquí (formatos permitidos: JPG, JPEG, PNG)",
            type=self.ALLOWED_IMAGE_FORMATS,
            accept_multiple_files=True,
        )
        return uploaded_images
