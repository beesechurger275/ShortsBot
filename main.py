import argparse
from redditscraper import RedditScraper
from pair import AudioThumbnailPair
from imagepost import ImagePostTemplate
from tts import TextToSpeech
from editfrompairs import video_from_pairs

a = (
    "comments",
    "image"
)

parser = argparse.ArgumentParser(
    prog="name",
    description="kill me",
    epilog="what the fuck"
)
parser.add_argument("subreddit", type=str)
parser.add_argument("numposts", type=int, nargs="?", const=5)
parser.add_argument("-t", "--type", type=str, nargs="?", const="image")
parser.add_argument("-o", "--output", type=str, nargs="?", const="out.mp4")
args = parser.parse_args()


if args.type not in a: exit(1)

scraper = RedditScraper()
tts = TextToSpeech()

pairs = []

if args.type == "image":
    posts = scraper.get_img_posts(args.subreddit).shuffle()
    i=0
    for post in posts:
        try: 
            ImagePostTemplate(post).draw().save(f"img_temp/img{i}.png")
            tts(post.title).save(f"audio_temp/audio{i}.mp3")
        except Exception as e: 
            continue

        pairs.append(AudioThumbnailPair(f"img_temp/img{i}.png", f"audio_temp/audio{i}.mp3"))
        i+=1
        if i > args.numposts: break

video_from_pairs(pairs, output=args.output)