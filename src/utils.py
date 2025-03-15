import os
import imghdr
from itertools import chain 

from PIL import Image
from PIL.Image import ImageFile


def __open_img_with_PIL(img_path: str) -> ImageFile.ImageFile:
    """Opens an image file using the Python Imaging Library (PIL).

    This function loads an image from the specified file path and returns it as 
    a PIL Image object.

    Args:
        img_path (str): The file path of the image to be opened.

    Returns:
        ImageFile.ImageFile: The opened image as a PIL Image object.
    """
    return Image.open(img_path)


def get_imgs_in_dir(dir_path: str) -> list[ImageFile.ImageFile]:
    """Finds and loads all valid images from a directory.

    This function scans the specified directory, detects valid image files, 
    and loads them as PIL Image objects.

    Args:
        dir_path (str): The path to the directory containing image files.

    Returns:
        list[ImageFile.ImageFile]: A list of loaded PIL Image objects.

    Raises:
        AssertionError: If the given directory path does not exist.
    """
    assert os.path.exists(dir_path), "The given path does not exist!"
    
    found_imgs: list[ImageFile.ImageFile] = []
    for file in os.listdir(dir_path):
        absolute_path: str = os.path.join(dir_path, file)
        
        if os.path.isfile(absolute_path) and imghdr.what(absolute_path):
            PIL_img: ImageFile.ImageFile = __open_img_with_PIL(absolute_path)           
            found_imgs.append(PIL_img)
            
    return found_imgs


def extract_raw_json(unparsed_json: str) -> str:
    """Extracts the pure JSON content.

    Args:
        unparsed_json (str): A JSON string potentially wrapped in Markdown-style 
                             triple backticks.

    Returns:
        str: The cleaned JSON string without Markdown formatting.
    """
    return unparsed_json.replace('```json\n', '')\
        .replace('\n```', '')


def flatten_list(array: list) -> list:
    return list(chain(*array))