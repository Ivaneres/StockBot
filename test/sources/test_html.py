import unittest
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
        data = html_parser.run()
        test_product = data[15]
        self.assertEqual(len(data), 264)
        self.assertEqual(test_product.name,
                         'Gigabyte NVIDIA GeForce RTX 3090 TURBO 24GB GDDR6X Ray-Tracing Graphics Card, 10496 Core, 1410MHz GPU, 1695MHz Boost')
        self.assertEqual(test_product.in_stock, True)
        self.assertEqual(test_product.price, '£1,998.98')


if __name__ == "__main__":
    unittest.main()
