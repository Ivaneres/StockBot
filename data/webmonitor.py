from typing import List, Dict, Union

import requests
import yaml

from data.api_parser import JSONSelector
from data.html_parser import HTMLSelector
from data.monitor import StockMonitor, Product

from bs4 import BeautifulSoup


class WebMonitor(StockMonitor):

    def __init__(
            self,
            data_type: str,
            selectors: List[Union[JSONSelector, HTMLSelector]],
            request_url: str,
            headers=None):
        if data_type not in ["api", "html"]:
            raise ValueError("data_type may only be api or html")
        if headers is None:
            headers = {}
        self.data_type = data_type
        self.headers = headers
        self.selectors = selectors
        self.request_url = request_url

    def get_data(self) -> Union[Dict, BeautifulSoup]:
        r = requests.get(url=self.request_url, headers=self.headers)
        if r.status_code != 200:
            raise ConnectionError(f"API returned non-200 code {r.status_code}")
        if self.data_type == "api":
            return r.json()
        return BeautifulSoup(r.content, "lxml")

    def run(self) -> List[Product]:
        data = self.get_data()
        return [x for selector in self.selectors for x in selector.parse_data(data)]

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, "r") as fp:
            data = yaml.safe_load(fp.read())
        selector_cls = JSONSelector if data["type"] == "api" else HTMLSelector
        selectors = [
            selector_cls(
                prod_path=x["products_path"],
                name_path=x["name_path"],
                stock_status_path=x["status_path"],
                stock_status_message=x["stock_message"],
                price_path=x.get("price_path")
            ) for x in data["selectors"]
        ]
        return cls(
            data_type=data["type"],
            request_url=data["url"],
            headers=data.get("headers"),
            selectors=selectors
        )
