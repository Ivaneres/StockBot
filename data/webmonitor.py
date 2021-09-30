import os
from typing import List, Dict, Union

import requests
import yaml

from data.json_selector import JSONSelector
from data.html_selector import HTMLSelector
from data.monitor import StockMonitor, Product, ProductCategory

from bs4 import BeautifulSoup


class WebMonitor(StockMonitor):

    def __init__(
            self,
            data_type: str,
            selectors: List[Union[JSONSelector, HTMLSelector]],
            request_url: str,
            headers=None,
            product_categories=None):
        if data_type not in ["api", "html"]:
            raise ValueError("data_type may only be api or html")
        if headers is None:
            headers = {}
        self.data_type = data_type
        self.headers = headers
        self.selectors = selectors
        self.request_url = request_url
        self.product_categories = product_categories

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
        return [x for selector in self.selectors for x in selector.parse_data(data, self.request_url)]

    @staticmethod
    def load_product_categories(paths: List[str]) -> List[ProductCategory]:
        product_categories = []
        for products_path in paths:
            base_path = os.path.normpath(products_path)
            for product in filter(lambda x: x.endswith(".yml"), os.listdir(products_path)):
                product_categories.append(ProductCategory.from_yaml(base_path + "/" + product))
        return product_categories

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, "r") as fp:
            data = yaml.safe_load(fp.read())
        product_categories = WebMonitor.load_product_categories(data.get("products", []))
        selectors = []
        for selector_data in data["selectors"]:
            default_args = {
                "prod_path": selector_data["products_path"],
                "name_path": selector_data["name_path"],
                "url_path": selector_data["url_path"],
                "image_url_path": selector_data["image_url_path"],
                "stock_status_path": selector_data["status_path"],
                "stock_status_message": selector_data["stock_message"],
                "price_path": selector_data.get("price_path"),
                "product_categories": product_categories
            }
            if data["type"] == "api":
                selector = JSONSelector(
                    **default_args
                )
            else:
                selector = HTMLSelector(
                    **default_args,
                    remove_classes=selector_data.get("remove_classes")
                )
            selectors.append(selector)
        return cls(
            data_type=data["type"],
            request_url=data["url"],
            headers=data.get("headers"),
            selectors=selectors,
            product_categories=product_categories
        )
