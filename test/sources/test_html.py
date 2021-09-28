import unittest
from bs4 import BeautifulSoup
import lxml
from data.html_parser import HTMLParser


class ScanTest(unittest.TestCase):
    def test_html_parser(self):
        html_parser = HTMLParser.from_yaml("./test/sources/scan_test.yml")
        self.assertEqual(len(html_parser.selectors), 1)
        self.assertEqual(html_parser.headers,
                         {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
        self.assertEqual(html_parser.request_url,
                         "https://www.scan.co.uk/shop/gaming/gpu-nvidia-gaming/3175/3176/3177/3221/3257/3350/3353")
        self.assertEqual(html_parser.selectors[0].prod_path, ["product"])
        self.assertEqual(html_parser.selectors[0].name_path, "description")
        self.assertEqual(html_parser.selectors[0].stock_status_message, "In stock")
        self.assertEqual(html_parser.selectors[0].status_path, "in stock")
        self.assertEqual(html_parser.selectors[0].price_path, "price")

    def test_HTML_selector(self):
        html_parser = HTMLParser.from_yaml("./test/sources/scan_test.yml")
        with open("./test/sources/test_html_data.html") as fp:
            soup = BeautifulSoup(fp, "lxml")
        data = html_parser.selectors[0].parse_data(soup)
        test_product = data[3]
        self.assertEqual(len(data), 264)
        self.assertEqual(test_product.name,
                         'ZOTAC NVIDIA GeForce RTX 3090 AMP Extreme Holo 24GB GDDR6X Ray-Tracing Graphics Card, 10496 Core, 1815MHz Boost')
        self.assertEqual(test_product.in_stock, True)
        self.assertEqual(test_product.price, 'Â£2,299.99')


if __name__ == "__main__":
    unittest.main()
