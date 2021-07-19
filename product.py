
class Product:
    """
    raw: varaible storing raw html / json of product to be indexed using selector
    selector: selector object used to index raw product data
    lisitng_type: string "JSON" or "HTML" indicating if product data was parsed from HTML or JSON data.
    source: string indicating source of product e.g. "NVIDIA", "Scan"
    """

    name = None
    in_stock = None
    price = None
    buy_link = None

    def __init__(self, raw , selector, listing_type: str, source: str):
        self.raw = raw
        self.selector = selector
        self.listing_type = listing_type
        self.source = source