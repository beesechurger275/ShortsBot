import requests
import json

class HTTPCodeNot200(Exception): 
    def __init__(self) -> None:
        super().__init__(f"Recieved non-200 status code")
        
defaults = {}

class URLJsonHandler:
    def __init__(self, headers:dict[str,str]=defaults) -> None:
        self.headers = headers

    def __call__(self, url:str) -> dict[str,object]:
        try: 
            return self.get_json(url)
        except HTTPCodeNot200:
            print("HTTP code not 200")
            return self.get_test_posts()

    def get_test_posts(self) -> dict[str,object]:
        with open("testdata/testdata.json", "r") as file: r = file.read()
        return json.loads(r)
    
    def get_test_sub_data(self) -> dict[str,object]:
        with open("testdata/testsubredditdata.json", "r") as file: r = file.read()
        return json.loads(r)

    def get_json(self, url:str) -> dict[str,object]:
        try:
            req = requests.get(url, headers=self.headers)
            if req.status_code == 200:
                return req.json()
        finally:
            raise HTTPCodeNot200