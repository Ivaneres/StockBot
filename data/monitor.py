from abc import ABC, abstractmethod
from typing import List


class Product:
    """
    raw: varaible storing raw html / json of product to be indexed using selector
    selector: selector object used to index raw product data
    lisitng_type: string "JSON" or "HTML" indicating if product data was parsed from HTML or JSON data.
    source: string indicating source of product e.g. "NVIDIA", "Scan"
    """

    def __init__(self, name: str, in_stock: bool, price: int):
        self.name = name
        self.in_stock = in_stock
        self.price = price


class StockMonitor(ABC):

    @abstractmethod
    def run(self) -> List[Product]:
        return NotImplemented
