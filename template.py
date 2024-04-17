from PIL import Image, ImageFont, ImageDraw, ImageOps
import textwrap

class Template:
    USER_FONT = ImageFont.truetype("img_assets/Arial.ttf", 25)
    BODY_FONT = ImageFont.truetype("img_assets/Arial.ttf", 30)
    UPVOTE_FONT = ImageFont.truetype("img_assets/Arial.ttf", 25)

    def __init__(self):
        ...

    def _wrap_text(self, text, width) -> tuple[str,int]:
        e = textwrap.wrap(text, width)
        return ("\n".join(e), len(e))

    def _format_num(self, input_:int) -> str:
        return str(input_)

    def _mask_profile_picture(self, image:Image.Image, size:tuple[int,int]=(50,50)) -> Image.Image:
        size = (50, 50)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + size, fill=255)

        return ImageOps.fit(image, mask.size, centering=(0.5,0.5)), mask

    def draw(self) -> Image.Image:
        ...