from abc import ABC, abstractmethod
from typing import Callable, List, Dict, Tuple, Optional
import requests
import json
from product import Product

class JsonSelector(object):
    """
    prod_path: path to find product entries from json data
    name_path: path to find product name from product entry
    status_path: path to find product status from product entry
    price_path: path to find product price from product entry
    """

    def __init__(self,
                 prod_path: List[str],
                 name_path: List[str], 
                 status_path: List[str], 
                 price_path: List[str] = None) -> None:
        
        self.prod_path = prod_path
        self.name_path = name_path
        self.status_path = status_path
        self.price_path = price_path
    
    def __iter__(self):
        for attr in self.__dict__.values():
            yield attr



class APIParser(ABC):
    headers: Dict[str, str]
    selectors: Tuple[JsonSelector]
    product_list: List[Tuple[Dict, Tuple]]
    request_url: str

    @abstractmethod
    def check_stock(self):
        raise NotImplementedError

    def get_product_data(self):
        # temp (no internet)
        r = requests.get(url=self.request_url, headers=self.headers)
        json_data = r.json()
        for selector in self.selectors:
            search_data = json_data.copy()
            for key in selector.prod_path:
                search_data = search_data[key]
                
            if not isinstance(search_data, dict):
                for product_dict in search_data:
                    self.product_list.append(Product(product_dict, selector, "JSON", "NVIDIA"))
            
            else:
                self.product_list.append(Product(search_data, selector, "JSON", "NVIDIA"))                  

