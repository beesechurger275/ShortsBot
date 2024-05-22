import requests
import json
from typing import Any

class HTTPCodeNot200(Exception): 
    def __init__(self) -> None:
        super().__init__(f"Recieved non-200 status code")
        
defaults = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class URLJsonHandler:
    def __init__(self, headers:dict[str,str]=defaults) -> None:
        self.headers = headers

    def __call__(self, url:str) -> dict[str,object]:
        return self.get_json(url)

    def get_test_posts(self) -> dict[str,object]:
        with open("testdata/testdata.json", "r") as file: r = file.read()
        return json.loads(r)
    
    def get_test_sub_data(self) -> dict[str,object]:
        with open("testdata/testsubredditdata.json", "r") as file: r = file.read()
        return json.loads(r)

    def get_json(self, url:str) -> dict[str,object]:
        req = requests.get(url, headers=self.headers)
        if req.status_code == 200:
            return req.json()
        raise HTTPCodeNot200
    
class FileJsonHandler:
    @staticmethod
    def get_json(file:str) -> Any:
        with open(file, "r") as f:
            a = json.loads(f.read())
        return a