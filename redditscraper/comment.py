from typing import Any
from . import kinds

class RedditComment:
    def __init__(self, data:dict[str,Any], get_replies=False, del_replies=False):
        self._dict = data["data"]

        if get_replies: self.get_replies()
        elif del_replies: self._del_replies() # memory/space savings

    def __getattr__(self, index:str) -> Any:
        return self._dict[index]
    
    def __delattr__(self, index:str) -> None:
        del self._dict[index]

    def _del_replies(self):
        del self.replies

    def _filter_reply(self, comment:"RedditComment") -> bool:
        return True # TODO

    def get_replies(self) -> None:
        """Replaces ```self.replies``` dict with list made of ```RedditComment``` instances"""
        if self.replies == "": 
            self.replies = []
            return
        
        new = []
        for reply in self.replies["data"]["children"]:
            if reply["kind"] != kinds.COMMENT: continue
            obj_ = RedditComment(reply)
            if self._filter_reply(obj_):
                new.append(obj_)
        self.replies = new

    def get_replies_recursive(self):
        pass