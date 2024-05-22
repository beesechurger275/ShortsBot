from PIL import Image
import requests
from io import BytesIO

# https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
def url_to_img(url:str) -> Image.Image:
    resp = requests.get(url)
    return Image.open(BytesIO(resp.content)).convert("RGBA")