from typing import ClassVar

from pandas import DataFrame
from streamlit import button, error, spinner, title
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.controller.streamlit_controller import StreamlitController
from src.service.base_service import BaseService
from src.view import (
    ImagesPreviewView,
    ImagesUploadView,
    MeetingsDownloadView,
    MeetingsPreviewView,
    MeetingsStatsView,
)
from src.view.base_view import BaseView


class StreamlitApp:
    PROCESS_IMAGES_ERROR: ClassVar[str] = (
        "⚠️ Ocurrió un error interno. Por favor, inténtalo de nuevo más tarde."
    )
    PREVIEW_IMAGES_ERROR: ClassVar[str] = (
        "⚠️ No se pudieron cargar las imágenes. Por favor, inténtalo de nuevo."
    )

    def __init__(self, service: BaseService):
        self.__views: list[BaseView] = [
            ImagesUploadView(),
            ImagesPreviewView(),
            MeetingsPreviewView(),
            MeetingsStatsView(),
            MeetingsDownloadView(),
        ]
        self.__controller = StreamlitController(service=service)

    def run(self) -> None:
        """
        Executes the main application flow.

        This method coordinates the following steps:
        1. Image upload and preview
        2. Image processing to extract meetings data
        3. Display of meetings information
        4. Generation of statistics
        5. Excel file download option

        Raises:
            Exception: If there's an error during image preview or processing.
                     These exceptions are caught and displayed as user-friendly messages.
        """
        title("Captura de Reuniones")
        (
            images_upload_view,
            images_preview_view,
            meetings_preview_view,
            meetings_stats_view,
            meetings_download_view,
        ) = self.__views
        uploaded_images: None | list[UploadedFile] = images_upload_view.render()
        if uploaded_images:
            try:
                images_preview_view.render(self.__controller.get_carousel_items(uploaded_images))
            except Exception:
                error(self.PREVIEW_IMAGES_ERROR)
                return

            if button("Procesar imágenes"):
                with spinner("Procesando imágenes, por favor espere..."):
                    try:
                        meetings_df: DataFrame = self.__controller.process_imgs(uploaded_images)
                    except Exception:
                        error(self.PROCESS_IMAGES_ERROR)
                        return

                meetings_preview_view.render(meetings_df)
                meetings_stats_view.render(len(uploaded_images), len(meetings_df))
                meetings_download_view.render(self.__controller.get_meetings_xlsx(meetings_df))
                return
