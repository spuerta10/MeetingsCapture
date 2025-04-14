from base64 import b64encode
from io import BytesIO

from pandas import DataFrame
from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.service.base_service import BaseService


class StreamlitController:
    """Controller for handling Streamlit app logic and interactions."""

    def __init__(self, service: BaseService):
        self.__service = service

    def get_carousel_items(self, uploaded_images: list[UploadedFile]) -> list[dict[str, str]]:
        """
        Converts uploaded images into carousel items with base64-encoded images.

        Args:
            uploaded_images (list[UploadedFile]): List of uploaded image files.

        Returns:
            list[dict[str, str]]: A list of dictionaries containing image metadata
            and base64-encoded images.
        """

        def img_to_base64(image: Image.Image) -> str:
            """
            Converts a PIL Image to a base64-encoded string.

            Args:
                image (Image.Image): The image to encode.

            Returns:
                str: The base64-encoded string of the image.
            """
            buffer: BytesIO = BytesIO()
            image.save(buffer, format=image.format)
            return b64encode(buffer.getvalue()).decode()

        carousel_items: list[dict[str, str]] = list()
        for file in uploaded_images:
            image: Image.Image = Image.open(file)
            img_base64: str = img_to_base64(image)
            carousel_items.append(
                {
                    "title": file.name,
                    "text": f"Image: {file.name}",
                    "img": f"data:image/png;base64,{img_base64}",
                }
            )
        return carousel_items

    def process_imgs(self, uploaded_images: list[UploadedFile]) -> DataFrame:
        """
        Processes uploaded images and returns a DataFrame with extracted data.

        Args:
            uploaded_images (list[UploadedFile]): List of uploaded image files.

        Returns:
            DataFrame: A DataFrame containing the processed data from the images.
        """
        return self.__service.execute(uploaded_images)

    def get_meetings_xlsx(self, meetings_df: DataFrame) -> bytes:
        """
        Converts a DataFrame of meetings into an Excel file for download.

        Args:
            meetings_df (DataFrame): The DataFrame containing meeting data.

        Returns:
            bytes: The Excel file content as a byte stream.
        """
        buffer: BytesIO = BytesIO()
        meetings_df.to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer.getvalue()
