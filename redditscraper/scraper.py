from .jsonhandler import URLJsonHandler
from .post import RedditPost
from typing import Any
from .postlist import PostList

default_options = {
    "headers": {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
}

class RedditScraper:
    def __init__(self, options:dict[str,Any]=default_options):
        self.jsonhandler = URLJsonHandler(headers=options['headers']) # TODO

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

    def _get_json(self, subreddit:str, **kwargs) -> list[RedditPost]:
        return self.jsonhandler.get_json(f"https://www.reddit.com/r/{subreddit}.json{RedditScraper._kwargs_to_str(**kwargs)}")
    
    def get_posts(self, subreddit:str, **kwargs) -> PostList:
        json = self._get_json(subreddit, **kwargs)
        return PostList.json_list_to_postlist(json["data"]["children"])