from typing import List, Dict
import requests
import yaml

from data.monitor import StockMonitor, Product
from utils import lookup


class JSONSelector:
    """
    prod_path: path to find product entries from json data
    name_path: path to find product name from product entry
    stock_status_path: path to find product stock status from product entry
    stock_status_message: stock_status_path value when the item is in stock. Optional - if not stock_status_path is not
        found, the item is assumed out of stock
    price_path: path to find product price from product entry
    """

    def __init__(
            self,
            prod_path: List[str],
            name_path: List[str],
            stock_status_path: List[str],
            stock_status_message: str = None,
            price_path: List[str] = None):
        self.prod_path = prod_path
        self.name_path = name_path
        self.status_path = stock_status_path
        self.stock_status_message = stock_status_message
        self.price_path = price_path

    def parse_data(self, data) -> List[Product]:
        products_data = lookup(data, self.prod_path)
        if isinstance(products_data, dict):
            # Forces products_data to always be a list, in case prod_path returns a singular item
            products_data = [products_data]
        return [Product(
            name=lookup(product, self.name_path),
            in_stock=lookup(product, self.status_path) == self.stock_status_message,
            price=lookup(product, self.price_path) if self.price_path is not None else None
        ) for product in products_data]


class APIParser(StockMonitor):

    def __init__(
            self,
            selectors: List[JSONSelector],
            request_url: str,
            headers=None):
        if headers is None:
            headers = {}
        self.headers = headers
        self.selectors = selectors
        self.request_url = request_url

    def get_api_data(self) -> Dict:
        r = requests.get(url=self.request_url, headers=self.headers)
        if r.status_code != 200:
            raise ConnectionError(f"API returned non-200 code {r.status_code}")
        return r.json()

    def run(self) -> List[Product]:
        json_data = self.get_api_data()
        return [x for selector in self.selectors for x in selector.parse_data(json_data)]

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, "r") as fp:
            data = yaml.safe_load(fp.read())
        selectors = [
            JSONSelector(
                prod_path=x["products_path"],
                name_path=x["name_path"],
                stock_status_path=x["status_path"],
                stock_status_message=x["stock_message"],
                price_path=x.get("price_path")
            ) for x in data["selectors"]
        ]
        return cls(
            request_url=data["url"],
            headers=data.get("headers"),
            selectors=selectors
        )
