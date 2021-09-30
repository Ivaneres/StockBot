from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import List, Optional

import yaml


class ProductCategory:

    def __init__(self, regex: str, name: str):
        self.regex = regex
        self.name = name

    def match(self, name: str) -> bool:
        return re.search(self.regex, name) is not None

    @staticmethod
    def find_from_list(lst: List[ProductCategory], name: str) -> Optional[ProductCategory]:
        name = name.lower()
        return next((x for x in lst if re.search(x.regex, name)), None)

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, "r") as fp:
            data = yaml.safe_load(fp.read())
        return cls(regex=data["match"], name=data["name"])


class Product:
    """
    raw: varaible storing raw html / json of product to be indexed using selector
    selector: selector object used to index raw product data
    lisitng_type: string "JSON" or "HTML" indicating if product data was parsed from HTML or JSON data.
    source: string indicating source of product e.g. "NVIDIA", "Scan"
    """

    def __init__(self, name: str, in_stock: bool, price: int, url: str, image_url: Optional[str] = None,
                 category: ProductCategory = None):
        self.name = name
        self.in_stock = in_stock
        self.price = price
        self.url = url
        self.image_url = image_url
        self.category = category


class StockMonitor(ABC):

    @abstractmethod
    def run(self) -> List[Product]:
        return NotImplemented
