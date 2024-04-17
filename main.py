import argparse

a = (
    "comments",
    "image"
)

parser = argparse.ArgumentParser(
    prog="TheNameIDontFuckingKnow",
    description="fucking kill me",
    epilog="what the fuck"
)
parser.add_argument("subreddit", type=str)
parser.add_argument("numposts", type=int, nargs="?", const=5)
parser.add_argument("-t", "--type", type=str, nargs="?", const="image")
args = parser.parse_args()
print(dict(args))


if args.type == "":
    pass