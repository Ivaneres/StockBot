from api_parser import JsonSelector, APIParser

# selectors = [JsonSelector(("searchedProducts", "productDetails", "displayName"),
#                          ("searchedProducts", "productDetails", "prdStatus")),
#            JsonSelector(("searchedProducts", "featuredProduct", "displayName"),
#                         ("searchedProducts", "featuredProduct", "prdStatus"))]

# NvidiaParser = APIParser(headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"},
#                          selectors = selectors,
#                          in_stock_text="in_stock",
#                          out_of_stock_text="out_of_stock")

# NvidiaParser.fetch(url = "https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-gb&category=GPU&"
#                          "gpu=RTX%203080,RTX%203070,RTX%203090&manufacturer=NVIDIA"
#                          "&manufacturer_filter=NVIDIA~3,ASUS~11,EVGA~4,GIGABYTE~11,MSI~6,PALIT~6,PNY~4,ZOTAC~6", 
#                          request_type = "GET")

class NvidiaParser(APIParser):
    selectors = (JsonSelector(["searchedProducts", "productDetails"], ["displayName"], ["prdStatus"]),
                 JsonSelector(["searchedProducts", "featuredProduct"], ["displayName"], ["prdStatus"]))

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }

    request_url = ("https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-gb&category=GPU&"
                  "gpu=RTX%203080,RTX%203070,RTX%203090&manufacturer=NVIDIA"
                  "&manufacturer_filter=NVIDIA~3,ASUS~11,EVGA~4,GIGABYTE~11,MSI~6,PALIT~6,PNY~4,ZOTAC~6")

    product_list = []

    def check_stock(self):
        if len(self.product_list) > 0:
            for product in self.product_list:
                # set product name
                for key in product.selector.name_path:
                    product.name = product.raw[key]

                # set product status
                for key in product.selector.status_path:
                    if product.raw[key] == "in_stock":
                        product.in_stock = True
                    elif product.raw[key] == "out_of_stock":
                        product.in_stock = False