from streamlit import download_button

from src.view.base_view import BaseView


class MeetingsDownloadView(BaseView):
    # @override
    def render(self, meetings_file: str) -> None:
        download_button(
            label="📥 Descargar Reuniones Detectadas",
            data=meetings_file,
            file_name="reuniones_detectadas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
