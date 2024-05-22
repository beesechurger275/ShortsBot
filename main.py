import argparse
from redditscraper import RedditScraper
from pair import AudioThumbnailPair
from imagepost import ImagePostTemplate
from textpost import TextPostTemplate
from comment import CommentTemplate
from tts import TextToSpeech
from editfrompairs import video_from_pairs
import random
import os

parser = argparse.ArgumentParser(
    prog="name",
    description="sdghugidsgfiodsjafg",
    epilog="what"
)
parser.add_argument("-s", "--subreddit", type=str, nargs="?")
parser.add_argument("-n", "--numposts", type=int, nargs="?", const=5)
parser.add_argument("-t", "--type", type=str, nargs="?", const="image")
parser.add_argument("-o", "--output", type=str, nargs="?", const="out.mp4")
parser.add_argument("-i", "--input", type=str, nargs="?", const=None)
args = parser.parse_args()

if args.type not in ("comments", "image"): exit(1)

scraper = RedditScraper()
tts = TextToSpeech()

pairs = []

offline = True if args.input is not None else False

vid_base = "videos/"+random.choice(os.listdir("videos/"))

if args.type == "image":
    if args.input is None:
        posts = scraper.get_img_posts(args.subreddit).shuffle()
    else:
        posts = scraper.from_json(args.input).shuffle() # TODO image filtering 

    i=0
    for post in posts:
        try: 
            ImagePostTemplate.draw(post, offline=offline).save(f"img_temp/img{i}.png")
            tts(post.title).save(f"audio{i}.mp3")
        except Exception as e: 
            print(f"1984: {e}")
            continue # files get overwritten as i is not incrimented

        pairs.append(AudioThumbnailPair(f"img_temp/img{i}.png", f"audio_temp/audio{i}.mp3"))
        i+=1
        if i >= args.numposts: break

elif args.type == "comments":
    if args.input is None:
        post = scraper.get_posts(args.subreddit).choice()
    else: 
        post = scraper.from_json(args.input).choice()

    post.get_comments()
    post.shuffle_comments()

    TextPostTemplate.draw(post, offline=offline).save("img_temp/img0.png")
    tts(post.title).save("audio0.mp3")
    pairs.append(AudioThumbnailPair("img_temp/img0.png", "audio_temp/audio0.mp3"))

    i=0
    for comment in post.comments:
        try:
            CommentTemplate.draw(comment, offline=offline).save(f"img_temp/img{i+1}.png")
            tts(comment.body).save(f"audio{i+1}.mp3")
        except Exception as e: 
            print(f"1984. {e}")
            continue 
        pairs.append(AudioThumbnailPair(f"img_temp/img{i+1}.png", f"audio_temp/audio{i+1}.mp3"))
        i+=1
        if i >= args.numposts: break


video_from_pairs(pairs, vid_base=vid_base, output=args.output)