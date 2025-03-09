import os
import imghdr
from itertools import chain 

from PIL import Image

def _open_img_with_PIL(img_path: str):
    return Image.open(img_path)


def get_imgs_in_dir(dir_path: str):
    assert os.path.exists(dir_path), "The given path does not exist!"
    
    found_imgs = []
    for file in os.listdir(dir_path):
        absolute_path = os.path.join(dir_path, file)
        
        if os.path.isfile(absolute_path) and imghdr.what(absolute_path):
            PIL_img = _open_img_with_PIL(absolute_path)           
            found_imgs.append(PIL_img)
            
    return found_imgs


def parse_json(unparsed_json: str):
    return (unparsed_json.replace('```json\n', '')).replace('\n```', '')


def flatten_list(array: list):
    return list(chain(*array))