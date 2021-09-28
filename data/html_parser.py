from typing import List
import requests
from bs4 import BeautifulSoup
import yaml

from data.monitor import StockMonitor, Product


class HTMLSelector:
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
            price_path: List[str] = None,
            remove_classes=None):
        if remove_classes is None:
            remove_classes = []
        self.prod_path = prod_path
        self.name_path = name_path
        self.status_path = stock_status_path
        self.stock_status_message = stock_status_message
        self.price_path = price_path
        self.remove_classes = remove_classes

    def parse_data(self, data) -> List[Product]:
        for cls in self.remove_classes:
            for tag in data.find_all(class_=cls):
                tag.decompose()

        products = data
        for path in self.prod_path[:-1]:
            products = products.find(class_=path)
        products = products.find_all(class_=self.prod_path[-1])

        result = []
        for product in products:
            name = product.find(class_=self.name_path).get_text().strip()
            status = product.find(class_=self.status_path)
            price = product.find(class_=self.price_path)
            result.append(Product(
                name=name,
                in_stock=self.stock_status_message.lower() in status.get_text().strip().lower() if status is not None else False,
                price=price.get_text().strip() if price is not None else None)
            )

        return result


class HTMLParser(StockMonitor):

    def __init__(
            self,
            selectors: List[HTMLSelector],
            request_url: str,
            headers=None):
        if headers is None:
            headers = {}
        self.headers = headers
        self.selectors = selectors
        self.request_url = request_url

    def run(self) -> List[Product]:
        r = requests.get(url=self.request_url, headers=self.headers)
        if r.status_code != 200:
            raise ConnectionError(f"API returned non-200 code {r.status_code}")
        html_data = r.content
        soup = BeautifulSoup(html_data, "lxml")
        return [x for selector in self.selectors for x in selector.parse_data(soup)]

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, "r") as fp:
            data = yaml.safe_load(fp.read())
        selectors = [
            HTMLSelector(
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
