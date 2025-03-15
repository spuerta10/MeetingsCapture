import json
from utils import extract_raw_json, flatten_list

from google.generativeai.generative_models import GenerativeModel
from PIL.JpegImagePlugin import JpegImageFile
from google.generativeai.types import GenerateContentResponse


def make_request_2_model(model: GenerativeModel, 
                         prompt: str, 
                         images: JpegImageFile | list[JpegImageFile]) -> list[dict]:
    """Makes a request to a generative model to structure image content into JSON format.

    Args:
        model (GenerativeModel): Generative model to make the request to.
        prompt (str): Prompt to be used in the request. 
        images (JpegImageFile | list[JpegImageFile]): Image or list of images to be used in the request.

    Returns:
        list[dict]: Structured images content in JSON format.
    """
    images: list[JpegImageFile] = list(images) if not isinstance(images, list) else images
    
    all_imgs_content: list[dict] = []
    for img in images:
        response: GenerateContentResponse = model.generate_content([prompt, img], stream=True)
        response.resolve()  # wait for the response to be ready
        parsed_json = extract_raw_json(response.text)
        all_imgs_content.append(json.loads(parsed_json))
    return flatten_list(all_imgs_content)