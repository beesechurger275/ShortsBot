from template import Template
from redditscraper import RedditPost
from PIL import Image, ImageDraw

class ImagePostTemplate(Template):
    @staticmethod
    def draw(post:RedditPost, *, offline=False) -> Image.Image:
        text_wrapped, lines = Template._wrap_text(post.title, 65)
        upvote_format = Template._format_num(post.ups)

        post_img = post.get_image()
        hperc = (800 / post_img.size[0])
        post_img = post_img.resize((800, int(post_img.size[1]*hperc)))

        width = 1000
        height = 100+lines*32+post_img.size[1]+90

        img = Image.new('RGBA', (width, height), Template.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        if not offline:
            profile_pic, mask = Template._mask_profile_picture(post.get_subreddit_icon())
            img.paste(profile_pic, (50,40), mask)
        # else: TODO

        top_text = "r/"+post.subreddit+" • u/"+post.author

        draw.text((110,50), top_text, font=Template.USER_FONT, fill=(0xE0,0xE0,0xE0,0xFF))
        draw.text((50,100), text_wrapped, font=Template.BODY_FONT, fill=(0xF0,0xF0,0xF0,0xFF))

        draw.text((90,height-55), upvote_format, font=Template.UPVOTE_FONT, fill=(0xE0,0xE0,0xE0,0xFF))

        img.paste(post_img, (100,150+((lines-1)*32)))

        upvote = Image.open("img_assets/upvote.png").resize((32,32))
        up_mask = Image.open("img_assets/upvote_mask.bmp").resize((32,32)).convert("L")
        img.paste(upvote, (50,height-60), up_mask)

        downvote = Image.open("img_assets/downvote.png").resize((32,32))
        down_mask = Image.open("img_assets/downvote_mask.bmp").resize((32,32)).convert("L")
        img.paste(downvote, (107+(11*len(upvote_format)),height-60), down_mask)

        return img