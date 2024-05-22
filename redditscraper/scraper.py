from .jsonhandler import URLJsonHandler, FileJsonHandler
from typing import Any
from .postlist import PostList
from .subreddit import Subreddit
from .post import RedditPost
import re

default_options = {
    "headers": {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        },
    "filetypes": (
        "png",
        "jpg",
        "jpeg",
        ),
    "tld-filter": (
        r"i\.redd\.it"
        ),
}

class RedditScraper:
    def __init__(self, options:dict[str,Any]={}):
        h = options['headers'] if 'headers' in options else default_options['headers']
        self.jsonhandler = URLJsonHandler(headers=h)
        self.options = options

        for option in default_options.keys():
            if option not in self.options:
                self.options[option] = default_options[option]

    @staticmethod
    def _kwargs_to_str(**kwargs:str) -> str:
        if len(kwargs) == 0: return ""
        str_ = ""
        a = False
        for i in kwargs.keys():
            if a:
                str_ += f"&{i}={kwargs[i]}"
                continue
            a = True
            str_ = f"?{i}={kwargs[i]}"

        return str_

    def _get_json(self, subreddit:str, **kwargs) -> dict[str,Any]:
        sort = '' 
        if 'sort' in kwargs: 
            sort = "/" + kwargs['sort']
            del kwargs['sort']

        return self.jsonhandler.get_json(f"https://www.reddit.com/r/{subreddit}{sort}.json{RedditScraper._kwargs_to_str(**kwargs)}")
    
    def _get_info_json(self, subreddit:str) -> dict[str,Any]:
        return self.jsonhandler.get_json(f"https://www.reddit.com/r/{subreddit}/about.json")

    def filter_img_tld(self, posts:PostList) -> PostList:
        post:RedditPost
        for post in posts:
            a = False
            for filter in self.options["tld-filter"]:
                if re.search(filter, post.url):
                    a = True
                    break
            if not a:
                posts.remove(post)
        return posts

    def get_posts(self, subreddit:str, **kwargs) -> PostList:
        json = self._get_json(subreddit, **kwargs)
        return PostList.json_list_to_postlist(json["data"]["children"])
    
    def get_info(self, subreddit:str) -> Subreddit:
        return Subreddit(self._get_info_json(subreddit))
    
    def get_img_posts(self, subreddit:str, **kwargs) -> PostList:
        posts = self.get_posts(subreddit, **kwargs)
        posts = self.filter_img_tld(posts)
        if len(posts) < 1: 
            raise Exception("no image posts found")
        return posts
    
    def from_json(self, file:str) -> PostList:
        json:list[dict[str,Any]] = FileJsonHandler.get_json(file)
        ret = PostList()
        for i in json:
            ret.append(RedditPost(i))
        return ret