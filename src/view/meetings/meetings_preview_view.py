from pandas import DataFrame
from streamlit import dataframe, divider, subheader, success

from src.view.base_view import BaseView


class MeetingsPreviewView(BaseView):
    # @override
    def render(self, meetings: DataFrame) -> None:
        success("✅ ¡Procesamiento completado con éxito!")
        subheader("Vista previa de las reuniones procesadas")
        dataframe(meetings, use_container_width=True)
        divider()
