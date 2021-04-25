from typing import Callable, List, Tuple, Union
from bs4 import BeautifulSoup
import requests


class TreeSelector:

    def __init__(self, html_tag: str, classes: List = None, index: int = 0):
        if classes is None:
            classes = []
        self.html_tag = html_tag
        self.classes = classes
        self.index = index


class SubelementSelector:

    def __init__(self, selectors: List[TreeSelector], attribute: str):
        self.selectors = selectors
        self.attribute = attribute

    def select(self, parent: BeautifulSoup) -> str:
        for selector in self.selectors:
            tag = selector.html_tag
            classes = selector.classes
            index = selector.index
            if index == 0:
                parent = parent.find(tag, classes)
            else:
                parent = parent.find_all(tag, classes)[index]
        if self.attribute == "text":
            return parent.getText()
        return parent[self.attribute]


class Scraper:

    def __init__(self, parser: str, root: TreeSelector, subelem_selectors=None, postprocess: Callable[[List], list] = lambda x: x):
        if subelem_selectors is None:
            subelem_selectors = []
        self.parser = parser
        self.root = root
        self.subelem_selectors = subelem_selectors
        self.postprocess = postprocess

    def scrape(self, url: str) -> List:
        r = requests.get(url)
        if r.status_code != 200:
            raise ConnectionError("Could not GET url")
        soup = BeautifulSoup(r.text, self.parser)
        elements = soup.find_all(self.root.html_tag, self.root.classes)
        res = []
        for elem in elements:
            res.append([selector.select(elem) for selector in self.subelem_selectors])
        return self.postprocess(res)
