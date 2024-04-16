from redditscraper import RedditScraper

scraper = RedditScraper()

postlist = scraper.get_posts("askreddit")

target = postlist[0]
target.get_comments()

print(target.title)

for i in range(0,5):
    print(target.comments[i].body)