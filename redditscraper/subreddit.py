from typing import Any
from PIL import Image
from .url_to_img import url_to_img

class Subreddit:
    def __init__(self, data:dict[str,Any]):
        self.data = data["data"]

    def __getattr__(self, index: str) -> Any:
        return self.data[index]

    def get_thumbnail(self) -> Image.Image:
        return url_to_img(self["icon_img"])