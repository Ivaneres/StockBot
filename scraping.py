from typing import Dict

import json
import requests

class NVIDIAScraper(Scraper):

    def __init__(self):
        self.request_url = "https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-gb&category=GPU&gpu=RTX%203080,RTX%203070,RTX%203090&manufacturer=NVIDIA&manufacturer_filter=NVIDIA~3,ASUS~11,EVGA~4,GIGABYTE~11,MSI~6,PALIT~6,PNY~4,ZOTAC~6"

    def check_stock(self) -> Dict[str, bool]:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        response_json = requests.get(self.request_url, headers=headers)
        data = json.loads(response_json.content)
        product_listings = {}
        for product in data["searchedProducts"]["productDetails"] + [data["searchedProducts"]["featuredProduct"]]:
            product_status = product["prdStatus"] == "out_of_stock"
            product_listings[product["displayName"]] = product_status
        return product_listings
