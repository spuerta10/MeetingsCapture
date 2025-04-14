from streamlit import columns, metric, subheader

from src.view.base_view import BaseView


class MeetingsStatsView(BaseView):
    # @override
    def render(self, total_uploaded_images: int, total_detected_meetings: int) -> None:
        subheader("📊 Aquí tienes un resumen de la información obtenida de las imágenes")
        left, center, right = columns(3)

        with left:
            metric(label="Total de Imágenes Subidas", value=total_uploaded_images)
        with center:
            metric(label="Total de Reuniones Detectadas", value=total_detected_meetings)
