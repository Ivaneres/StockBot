from typing import List
from bs4 import BeautifulSoup

from data.monitor import Product, ProductCategory
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
            product_categories: List[ProductCategory],
            prod_path: List[str],
            name_path: List[str],
            url_path: List[str],
            stock_status_path: List[str],
            stock_status_message: str = None,
            image_url_path: List[str] = None,
            price_path: List[str] = None):
        self.product_categories = product_categories
        self.prod_path = prod_path
        self.name_path = name_path
        self.url_path = url_path
        self.status_path = stock_status_path
        self.stock_status_message = stock_status_message
        self.image_url_path = image_url_path
        self.price_path = price_path

    def parse_data(self, data: BeautifulSoup, request_url: str) -> List[Product]:
        products_data = lookup(data, self.prod_path)
        if isinstance(products_data, dict):
            # Forces products_data to always be a list, in case prod_path returns a singular item
            products_data = [products_data]
        return [
            Product(
                name=name,
                in_stock=lookup(product, self.status_path) == self.stock_status_message,
                price=lookup(product, self.price_path) if self.price_path is not None else None,
                url=lookup(product, self.url_path),
                image_url=lookup(product, self.image_url_path) if self.image_url_path is not None else None,
                category=ProductCategory.find_from_list(self.product_categories, name)
            ) for product in products_data if (name := lookup(product, self.name_path))]
