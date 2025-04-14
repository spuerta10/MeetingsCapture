from typing import ClassVar

from streamlit import subheader
from streamlit_carousel import carousel

from src.view.base_view import BaseView


class ImagesPreviewView(BaseView):
    CAROUSEL_ITEM_KEYS_ERROR: ClassVar[str] = (
        "All carousel items must contain title, text, and img keys"
    )

    REQUIRED_CAROUSEL_KEYS: ClassVar[list[str]] = ["title", "text", "img"]

    # @override
    def render(self, carousel_imgs: list[dict[str, str]]) -> None:
        assert all(
            all(key in item for key in self.REQUIRED_CAROUSEL_KEYS) for item in carousel_imgs
        ), self.CAROUSEL_ITEM_KEYS_ERROR

        subheader("Vista previa de las imágenes")
        carousel(
            items=carousel_imgs,
            slide=True,
            fade=False,
            controls=True,
            indicators=False,
            interval=3000,
            pause="hover",
            wrap=True,
            container_height=700,
            width=1,
        )
