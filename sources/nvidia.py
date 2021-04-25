import data.api_parser as ap

class NvidiaParser:
    selectors = [ap.JSONSelector(["searchedProducts", "productDetails", "prdStatus"]),
                 ap.JSONSelector(["searchedProducts", "featuredProduct", "prdStatus"])]

    parser = ap.APIParser(selectors)
    request_url = "https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-gb&category=GPU&gpu=RTX%203080,RTX%203070,RTX%203090&manufacturer=NVIDIA&manufacturer_filter=NVIDIA~3,ASUS~11,EVGA~4,GIGABYTE~11,MSI~6,PALIT~6,PNY~4,ZOTAC~6"


    def check_stock(self):
        self.parser.fetch(self.request_url, "GET")