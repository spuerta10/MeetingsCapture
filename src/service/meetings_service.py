from dataclasses import dataclass, field
from itertools import chain
from json import loads
from typing import ClassVar

import google.generativeai as genai
from google.generativeai.generative_models import GenerativeModel
from google.generativeai.types import GenerateContentResponse
from pandas import DataFrame
from PIL import Image
from PIL.ImageFile import ImageFile
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.service.base_service import BaseService


@dataclass
class MeetingsService(BaseService):
    GENAI_CONFIG_ERROR: ClassVar[str] = (
        "Failed to configure Generative AI model. Please check your API key."
    )
    HEARTBEAT_ERROR: ClassVar[str] = "Heartbeat check failed. Please check your model type."

    gemini_api_secret: str
    model_type: str
    prompt: str
    model: GenerativeModel = field(init=False)

    def __post_init__(self) -> None:
        """
        Initializes and configures the Gemini AI model.

        This method runs after dataclass initialization to:
        1. Configure the Gemini AI client with the provided API key
        2. Initialize the specified model type
        3. Perform a health check to ensure model availability

        Raises:
            RuntimeError: If model configuration fails or health check fails
        """
        try:
            genai.configure(api_key=self.gemini_api_secret)
        except Exception as e:
            raise RuntimeError(self.GENAI_CONFIG_ERROR) from e
        else:
            self.model = genai.GenerativeModel(self.model_type)
            if not self.__heartbeat():
                raise RuntimeError(self.HEARTBEAT_ERROR)

    def __heartbeat(self) -> bool:
        """
        Performs a health check on the configured Gemini AI model.

        Sends a simple test prompt to verify that the model:
        1. Is accessible
        2. Can process requests
        3. Returns valid responses

        Returns:
            bool: True if model is healthy and responding, False otherwise
        """
        try:
            heartbeat_response: GenerateContentResponse = self.model.generate_content(
                ["heartbeat check"], stream=False
            )
            return heartbeat_response is not None and hasattr(heartbeat_response, "text")
        except Exception:
            return False

    # @override
    def execute(self, uploaded_images: list[UploadedFile]) -> DataFrame:
        """
        Processes a list of images to extract meeting information using Gemini AI.

        Takes uploaded images, processes them through the AI model using the configured
        prompt, and consolidates the results into a structured DataFrame.

        Args:
            uploaded_images (list[UploadedFile]): List of uploaded image files to process

        Returns:
            DataFrame: Structured data containing extracted meeting information from images.
                      Each row represents a meeting entry with its corresponding details.
        """
        PIL_imgs: list[ImageFile] = [Image.open(file) for file in uploaded_images]
        imgs_content: list[dict] = list()
        for img in PIL_imgs:
            response: GenerateContentResponse = self.model.generate_content(
                [self.prompt, img], stream=True
            )
            response.resolve()  # wait for the response to be ready
            parsed_content: str = response.text.replace("```json\n", "").replace("\n```", "")
            imgs_content.append(loads(parsed_content))
        return DataFrame(list(chain(*imgs_content)))  # flatten imgs content list
