from typing import Union, Any
from jsonhandler import URLJsonHandler
import kinds
from comment import RedditComment

class RedditPost:
    def __init__(self, data:Union[dict[str,Any], list[dict[str,Any]]], settings:dict={}, get_comments=False):
        if data["kind"] != kinds.LINK and data["kind"] != "Listing": raise Exception # reddit devs smoking crack again

        if isinstance(data, dict): self._dict = data['data']
        else: self._dict = data[0]["data"] # allows posts to be passed from both their .json url and subreddit jsons

        self.settings = settings

        self.comments = []
        if get_comments: self.get_comments()

    def __getattr__(self, index:str) -> Any:
        return self._dict[index]
    
    def _filter_comment(self, comment:RedditComment):
        return True # TODO

    def get_comments(self) -> None:
        """Loads comments into the ```RedditPost``` structure."""
        handler = URLJsonHandler() # TODO FIXME headers (fix defaults in jsonhandler.py)
        json = handler.get_json(self.url[:-1] + ".json") # chop off trailing slash and add .json

        if len(json) < 2: raise Exception 

        comments = json[1]["data"]["children"]
        for comment in comments:
            if comment["kind"] != kinds.COMMENT: continue # skip non-comments
            comm_obj = RedditComment(comment)
            if self._filter_comment(comm_obj):
                self.comments.append(comm_obj)

    def get_comments_recursive(self) -> None:
        """This is a bad idea"""
        pass