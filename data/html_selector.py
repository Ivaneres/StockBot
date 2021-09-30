from typing import List
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from price_parser import Price

from data.monitor import Product, ProductCategory


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
            product_categories: List[ProductCategory],
            prod_path: List[str],
            name_path: List[str],
            url_path: List[str],
            stock_status_path: List[str],
            stock_status_message: str = None,
            image_url_path: List[str] = None,
            price_path: List[str] = None,
            remove_classes=None):
        if remove_classes is None:
            remove_classes = []
        self.product_categories = product_categories
        self.prod_path = prod_path
        self.name_path = name_path
        self.url_path = url_path
        self.status_path = stock_status_path
        self.stock_status_message = stock_status_message
        self.image_url_path = image_url_path
        self.price_path = price_path
        self.remove_classes = remove_classes

    def parse_data(self, data: BeautifulSoup, request_url: str) -> List[Product]:
        request_url_parse = urlparse(request_url)
        request_url_base = request_url_parse.scheme + "://" + request_url_parse.netloc

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
            url_obj = product.find(class_=self.url_path)
            if url_obj.name != "a":
                url_obj = url_obj.find("a")
            url = url_obj.get("href")
            image_url = None
            if self.image_url_path is not None:
                image_obj = product.find("img", class_=self.image_url_path)
                if image_obj is not None:
                    image_url = image_obj.get("src")
            result.append(
                Product(
                    name=name,
                    in_stock=self.stock_status_message.lower() in status.get_text().strip().lower() if status is not None else False,
                    price=Price.fromstring(price.get_text().strip()) if price is not None else None,
                    url=urljoin(request_url_base, url),
                    image_url=image_url,
                    category=ProductCategory.find_from_list(self.product_categories, name)
                ),
            )

        return result
