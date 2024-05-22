from PIL import Image, ImageFont, ImageDraw, ImageOps
import textwrap

class Template:
    USER_FONT = ImageFont.truetype("img_assets/Arial.ttf", 25)
    BODY_FONT = ImageFont.truetype("img_assets/Arial.ttf", 30)
    UPVOTE_FONT = ImageFont.truetype("img_assets/Arial.ttf", 25)

    BACKGROUND_COLOR = (0x0F,0x0F,0x0F)

    @staticmethod
    def _wrap_text(text, width) -> tuple[str,int]:
        e = textwrap.wrap(text, width)
        return ("\n".join(e), len(e))

    @staticmethod
    def _format_num(input_:int) -> str:
        return str(input_)

    @staticmethod
    def _mask_profile_picture(image:Image.Image, size:tuple[int,int]=(50,50)) -> Image.Image:
        size = (50, 50)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + size, fill=255)

        return ImageOps.fit(image, mask.size, centering=(0.5,0.5)), mask

    @staticmethod
    def draw() -> Image.Image:
        ...