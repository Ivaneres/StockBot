import json
import unittest
from unittest.mock import patch

import data
from data.api_parser import APIParser
from data.webmonitor import WebMonitor


class NvidiaTest(unittest.TestCase):
    def test_yaml_parser(self):
        nvidia_parser = APIParser.from_yaml("./sources/nvidia.yml")
        self.assertEqual(len(nvidia_parser.selectors), 2)
        self.assertEqual(nvidia_parser.headers, {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
        self.assertEqual(nvidia_parser.request_url, "https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-gb&category=GPU&gpu=RTX%203080,RTX%203070,RTX%203090&manufacturer=NVIDIA&manufacturer_filter=NVIDIA~3,ASUS~11,EVGA~4,GIGABYTE~11,MSI~6,PALIT~6,PNY~4,ZOTAC~6")
        self.assertEqual(nvidia_parser.selectors[1].stock_status_message, "in_stock")
        self.assertEqual(nvidia_parser.selectors[0].prod_path, ["searchedProducts", "productDetails"])
        self.assertEqual(nvidia_parser.selectors[0].price_path, ["productPrice"])
        self.assertEqual(nvidia_parser.selectors[1].name_path, ["displayName"])

    @patch("data.api_parser.JSONSelector")
    def test_api_parser(self, MockJSONSelector):
        json_selector_1 = data.api_parser.JSONSelector(
                    prod_path=["testing"],
                    price_path=["price"],
                    name_path=["name"],
                    stock_status_path=["status"],
                    stock_status_message="status_message"
                )
        json_selector_2 = data.api_parser.JSONSelector(
                    prod_path=["testing2"],
                    name_path=["name2"],
                    stock_status_path=["status2"],
                )
        api_parser = APIParser(
            selectors=[json_selector_1, json_selector_2],
            headers={"Example-Header": "HeaderValue"},
            request_url="https://a-totally-legit-url.com/a-page?product=gfx-card"
        )
        test_data = {
            "testing": {
                "price": 1,
                "name": "aaaaaa",
                "status": "no",
            },
            "testing2": {
                "name2": "aaaaaa",
                "status2": "no",
            }
        }
        with patch.object(APIParser, "get_api_data", return_value=test_data):
            api_parser.run()
        self.assertTrue(json_selector_1.parse_data.called)
        self.assertTrue(json_selector_2.parse_data.called)
        self.assertEqual(json_selector_1.parse_data.call_args[0][0], json_selector_2.parse_data.call_args[0][0])
        self.assertTrue("testing" in json_selector_1.parse_data.call_args[0][0].keys())

    def test_json_selector(self):
        nvidia_parser = WebMonitor.from_yaml("./sources/nvidia.yml")
        with open("./test/sources/test_nvidia_data.json", "r") as fp:
            data = json.load(fp)
        parsed_0 = nvidia_parser.selectors[0].parse_data(data)
        self.assertEqual(len(parsed_0), 2)
        self.assertEqual(parsed_0[0].name, "NVIDIA RTX 3090")
        self.assertEqual(parsed_0[0].in_stock, False)
        self.assertEqual(parsed_0[1].price, "£469.00")
        parsed_1 = nvidia_parser.selectors[1].parse_data(data)
        self.assertEqual(len(parsed_1), 1)
        self.assertEqual(parsed_1[0].name, "NVIDIA RTX 3080")


if __name__ == "__main__":
    unittest.main()
