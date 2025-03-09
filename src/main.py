import config
import os
from model_request import make_request_2_model
from utils import get_imgs_in_dir

import google.generativeai as genai
import pandas as pd

API_KEY, PROMPT = os.environ["GEMINI_API_KEY"], os.environ["PROMPT"]

genai.configure(api_key=API_KEY)

MODEL = genai.GenerativeModel('gemini-1.5-flash')

imgs = get_imgs_in_dir(r"../img/25-02-2025/")

events = make_request_2_model(model=MODEL,
                    prompt=PROMPT,
                    img=imgs)

df = pd.DataFrame(events)
df.to_excel("C:\\Users\\Admin\\Desktop\\agendaEdison\\out\\reuniones_2024.xlsx")