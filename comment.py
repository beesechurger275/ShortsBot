from template import Template
from PIL import Image, ImageDraw
from redditscraper import RedditComment
import random
import os

class CommentTemplate(Template):
    @staticmethod
    def draw(comment:RedditComment, *, offline=False) -> Image.Image:
        text_wrapped, lines = Template._wrap_text(comment.body, 65)
        upvote_format = Template._format_num(comment.ups)

        width = 1000
        height = 100+lines*32+75

        img = Image.new('RGBA', (width, height), Template.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        profile_pic, mask = Template._mask_profile_picture(Image.open("img_assets/profile_pic/"+random.choice(os.listdir("img_assets/profile_pic/"))))
        img.paste(profile_pic, (50,40), mask)

        draw.text((110,50), "u/"+comment.author, font=Template.USER_FONT, fill=(0xE0,0xE0,0xE0,0xFF))
        draw.text((50,100), text_wrapped, font=Template.BODY_FONT, fill=(0xF0,0xF0,0xF0,0xFF))

        draw.text((90,height-55), upvote_format, font=Template.UPVOTE_FONT, fill=(0xE0,0xE0,0xE0,0xFF))

        upvote = Image.open("img_assets/upvote.png").resize((32,32))
        up_mask = Image.open("img_assets/upvote_mask.bmp").resize((32,32)).convert("L")
        img.paste(upvote, (50,height-60), up_mask)

        downvote = Image.open("img_assets/downvote.png").resize((32,32))
        down_mask = Image.open("img_assets/downvote_mask.bmp").resize((32,32)).convert("L")
        img.paste(downvote, (107+(11*len(upvote_format)),height-60), down_mask)

        return img