from abc import ABC, abstractmethod
from typing import List, Optional


class Product:
    """
    raw: varaible storing raw html / json of product to be indexed using selector
    selector: selector object used to index raw product data
    lisitng_type: string "JSON" or "HTML" indicating if product data was parsed from HTML or JSON data.
    source: string indicating source of product e.g. "NVIDIA", "Scan"
    """

    def __init__(self, name: str, in_stock: bool, price: int, url: str, image_url: Optional[str] = None):
        self.name = name
        self.in_stock = in_stock
        self.price = price
        self.url = url
        self.image_url = image_url


class StockMonitor(ABC):

    @abstractmethod
    def run(self) -> List[Product]:
        return NotImplemented
