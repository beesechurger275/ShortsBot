from typing import Union, Any
from .jsonhandler import URLJsonHandler, FileJsonHandler
from . import kinds
from .comment import RedditComment
from .url_to_img import url_to_img
import re
from PIL import Image
import random

class NoImage(Exception): pass

class RedditPost:
    def __init__(self, data:Union[dict[str,Any], list[dict[str,Any]]], settings:dict={}, get_comments=False):
        if data["kind"] != kinds.LINK and data["kind"] != "Listing": raise Exception # reddit devs smoking crack again

        if isinstance(data, dict): self._dict = data['data']
        else: self._dict = data[0]["data"] # allows posts to be passed from both their .json url and subreddit jsons

        self.settings = settings

        self.comments = None
        if get_comments: self.get_comments()

        self.icon = None

    def __getattr__(self, index:str) -> Any:
        return self._dict[index]
    
    def __str__(self) -> str:
        reg = re.findall(r"^https:\/\/reddit.com(.*)$", self.url)
        reg = reg[0] if len(reg) > 0 else False
        return f"""Subreddit: {self.subreddit_name_prefixed}
Title: {self.title}
Author: u/{self.author}
{'''
''' + self.url if reg != self.permalink else ""}{'''
''' + self.selftext if len(self.selftext) > 0 else ""}
        """

    def _filter_comment(self, comment:RedditComment):
        return True # TODO

    def json(self) -> dict[str,Any]:
        return self._dict

    def get_image(self) -> Image.Image:
        reg = re.findall(r"^https:\/\/reddit.com(.*)$", self.url)
        reg = reg[0] if len(reg) > 0 else False 
        if reg == self.permalink:
            raise NoImage("no image associated with this post!")
        return url_to_img(self.url)

    def get_comments(self) -> None:
        """Loads comments into the ```RedditPost``` structure."""
        from .postlist import PostList # TODO bad?
        self.comments = PostList()

        if self.permalink[:5] != "json:": # TODO
            handler = URLJsonHandler()
            json = handler.get_json("https://reddit.com"+self.permalink[:-1] + ".json") # chop off trailing slash and add .json

            if len(json) < 2: raise Exception 

            comments = json[1]["data"]["children"]
        else:
            spl:list[str] = self.permalink.split(":")
            json:list[dict[str,Any]] = FileJsonHandler.get_json(spl[1])
            this:dict[str,Any] = json[int(spl[2])]
            comments = this["data"]["comments"]


        for comment in comments:
            if comment["kind"] != kinds.COMMENT: continue # skip non-comments
            comm_obj = RedditComment(comment)
            if self._filter_comment(comm_obj):
                self.comments.append(comm_obj)

    def shuffle_comments(self) -> None:
        random.shuffle(self.comments)

    def get_comments_recursive(self) -> None:
        """This is a bad idea"""
        pass

    def get_subreddit_icon(self):
        if self.icon is None:
            a = URLJsonHandler().get_json(f"https://www.reddit.com/r/{self.subreddit}/about.json")
            self.icon = url_to_img(re.findall(r"^(.*)\?.*$", a["data"]["community_icon"])[0])
        return self.icon
    
    # type hinting
    permalink:str
    url:str
    title:str
    author:str
    selftext:str
    subreddit:str
    subreddit_name_prefixed:str
    ups:int