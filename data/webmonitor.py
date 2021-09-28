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
        else:
            return BeautifulSoup(r.content, "lxml")

    def run(self) -> List[Product]:
        data = self.get_data()
        return [x for selector in self.selectors for x in selector.parse_data(data)]

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, "r") as fp:
            data = yaml.safe_load(fp.read())
        selectors = []
        for selector_data in data["selectors"]:
            if data["type"] == "api":
                selector = JSONSelector(
                    prod_path=selector_data["products_path"],
                    name_path=selector_data["name_path"],
                    stock_status_path=selector_data["status_path"],
                    stock_status_message=selector_data["stock_message"],
                    price_path=selector_data.get("price_path")
                )
            else:
                selector = HTMLSelector(
                    prod_path=selector_data["products_path"],
                    name_path=selector_data["name_path"],
                    stock_status_path=selector_data["status_path"],
                    stock_status_message=selector_data["stock_message"],
                    price_path=selector_data.get("price_path"),
                    remove_classes=selector_data.get("remove_classes")
                )
            selectors.append(selector)
        return cls(
            data_type=data["type"],
            request_url=data["url"],
            headers=data.get("headers"),
            selectors=selectors
        )
