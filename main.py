from pyconfparser import ConfigFactory
import google.generativeai as genai
from PIL.Image import ImageFile
from pandas import DataFrame

from conf.schema import ConfigurationSchema
from utils import get_imgs_in_dir
from model_request import make_request_2_model

if __name__ == "__main__":
    conf = ConfigFactory.get_conf(r"conf/config.json", ConfigurationSchema)
    genai.configure(api_key=conf.gemini_api_key)
    MODEL = genai.GenerativeModel(conf.model_type)
    
    imgs: list[ImageFile.ImageFile] = get_imgs_in_dir(r"../img/25-02-2025/")
    imgs_structured_content: list[dict] = make_request_2_model(
        model=MODEL,
        prompt=conf.prompt,
        images=imgs
    )
    df: DataFrame = DataFrame(imgs_structured_content)
    df.to_excel(conf.file_path + "reuniones_2024.xlsx")  # TODO: improve this with filepath join