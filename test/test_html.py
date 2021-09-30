import unittest
from bs4 import BeautifulSoup
from data.webmonitor import WebMonitor


class HTMLSourceTest(unittest.TestCase):
    def test_html_parser(self):
        html_parser = WebMonitor.from_yaml("./test/sources/scan_test.yml")
        self.assertEqual(len(html_parser.selectors), 1)
        self.assertEqual(html_parser.headers,
                         {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
        self.assertEqual(html_parser.request_url,
                         "https://www.scan.co.uk/shop/gaming/gpu-nvidia-gaming/3175/3176/3177/3221/3257/3350/3353")
        self.assertEqual(html_parser.data_type, "html")
        self.assertEqual(html_parser.selectors[0].prod_path, ["product"])
        self.assertEqual(html_parser.selectors[0].name_path, "description")
        self.assertEqual(html_parser.selectors[0].stock_status_message, "In stock")
        self.assertEqual(html_parser.selectors[0].status_path, "in stock")
        self.assertEqual(html_parser.selectors[0].price_path, "price")

    def test_HTML_selector(self):
        html_parser = WebMonitor.from_yaml("./test/sources/scan_test.yml")
        with open("./test/sources/test_html_data.html") as fp:
            soup = BeautifulSoup(fp, "lxml")
        data = html_parser.selectors[0].parse_data(soup, "https://google.com/some_product/")
        test_product = data[1]
        self.assertEqual(len(data), 3)
        self.assertEqual(test_product.name,
                         'ZOTAC NVIDIA GeForce RTX 3090 AMP Extreme Holo 24GB GDDR6X Ray-Tracing Graphics Card, 10496 Core, 1815MHz Boost')
        self.assertEqual(test_product.in_stock, True)
        self.assertEqual(test_product.price.amount_float, 2299.99)
        self.assertEqual(test_product.category.name, "RTX 3090")
        self.assertEqual(test_product.url, "https://www.scan.co.uk/products/zotac-nvidia-geforce-rtx-3090-amp-extreme-holo-24gb-gddr6x-ray-tracing-graphics-card-10496-core-1815")


if __name__ == "__main__":
    unittest.main()
