import json
from utils import parse_json, flatten_list

from google.generativeai.generative_models import GenerativeModel
from PIL.JpegImagePlugin import JpegImageFile


def make_request_2_model(model: GenerativeModel, 
                         prompt: str, 
                         img: JpegImageFile | list[JpegImageFile]) -> list:
    if not isinstance(img, list):
        img = list(img)
    
    all_imgs_content = []
    for i in img:
        response = model.generate_content([prompt, i], stream= True)
        response.resolve()
        parsed_json = parse_json(response.text)
        all_imgs_content.append(json.loads(parsed_json))
    return flatten_list(all_imgs_content)