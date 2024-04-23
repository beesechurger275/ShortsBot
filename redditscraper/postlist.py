from typing import Any
from collections.abc import Sequence
import random
from .post import RedditPost

class PostList(Sequence):
    def __init__(self, li:list[RedditPost]=None): 
        self._list = li if li is not None else [] # avoids mutable default shenanegans

        super().__init__()

    def __getitem__(self, index:int) -> RedditPost:
        return self._list[index]
    
    def __len__(self) -> int:
        return len(self._list)

    def __str__(self) -> str:
        return str(self._list) # TODO?

    def __delattr__(self, index: str) -> None:
        del self._list[index]

    def append(self, item:RedditPost) -> None:
        self._list.append(item)

    def remove(self, item:RedditPost) -> None:
        self._list.remove(item)

    def shuffle(self) -> "PostList":
        random.shuffle(self._list)
        return self
    
    def choice(self) -> RedditPost:
        return random.choice(self._list)

    def json(self) -> list[dict[str, Any]]:
        return [i.json() for i in self._list]

    @staticmethod
    def json_list_to_postlist(li:list[dict[str,Any]]) -> "PostList":
        """Pass ```data->children``` from JSON, returns PostList with posts"""
        postlist = PostList()
        for i in li:
            postlist.append(RedditPost(i))

        return postlist
    
    @staticmethod
    def list_to_postlist(li:list[RedditPost]) -> "PostList":
        postlist = PostList()
        for i in li:
            postlist.append(i)

        return postlist