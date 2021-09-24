from abc import ABC, abstractmethod
from typing import List


class Product:
    """
    raw: varaible storing raw html / json of product to be indexed using selector
    selector: selector object used to index raw product data
    lisitng_type: string "JSON" or "HTML" indicating if product data was parsed from HTML or JSON data.
    source: string indicating source of product e.g. "NVIDIA", "Scan"
    """

    def __init__(self, raw, selector, listing_type: str, source: str, name: str, in_stock: bool, price: int,
                 buy_link: str):
        self.raw = raw
        self.selector = selector
        self.listing_type = listing_type
        self.source = source
        self.name = name
        self.in_stock = in_stock
        self.price = price
        self.buy_link = buy_link


class StockMonitor(ABC):

    @abstractmethod
    def run(self) -> List[Product]:
        return NotImplemented
