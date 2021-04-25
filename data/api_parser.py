from typing import Callable, List, Dict
import requests


class JSONSelector:

    def __init__(self, selection_path: List[str]):
        self.selection_path = selection_path

    def select(self, data: Dict):
        for key in self.selection_path:
            if isinstance(data, list) and not isinstance(key, int):
                raise RuntimeError("Attempted to index list with a non-int type.")
            if isinstance(data, list) and key >= len(data):
                raise RuntimeError("Index greater than list length")
            elif isinstance(data, dict) and data.get(key) is None:
                raise RuntimeError(f"Could not find key {key} in dict")
            data = data[key]
        return data

class APIParser:

    def __init__(self, selectors: List[JSONSelector], headers=None, postprocess: Callable = lambda x: x):
        if headers is None:
            headers = {}
        self.headers = headers
        self.selectors = selectors
        self.__postprocess = postprocess

    def fetch(self, url: str, request_type: str, data: Dict[str, str]) -> List[str]:
        if request_type not in ["GET", "POST"]:
            raise ValueError(f"{request_type} is not a valid request type")
        if request_type == "GET":
            r = requests.get(url, data, headers=self.headers)
        else:
            r = requests.post(url, json=data, headers=self.headers)
        data = r.json()
        return self.__postprocess([x.select(data) for x in self.selectors])
