from template import Template
from redditscraper import RedditPost
from PIL import Image, ImageDraw
import random

class ImagePostTemplate(Template):
    def __init__(self, post:RedditPost):
        self.post = post

    def draw(self) -> Image.Image:
        text_wrapped, lines = Template._wrap_text(self.post.title, 65)
        upvote_format = Template._format_num(self.post.ups)

        post_img = self.post.get_image()
        hperc = (800 / post_img.size[0])
        post_img = post_img.resize((800, int(post_img.size[1]*hperc)))

        width = 1000
        height = 100+lines*32+post_img.size[1]+90

        img = Image.new('RGBA', (width, height), Template.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        profile_pic, mask = self._mask_profile_picture(self.post.get_subreddit_icon())
        img.paste(profile_pic, (50,40), mask)

        top_text = "r/"+self.post.subreddit+" • u/"+self.post.author

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
    

if __name__ == "__main__":
    from redditscraper import RedditScraper
    scraper = RedditScraper()
    posts = random.choice(scraper.get_img_posts("furry", sort="top", t="week"))

    a = ImagePostTemplate(posts)
    img = a.draw()
    img.save("test.png")
