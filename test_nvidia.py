import json
import time
import requests

url = "https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-gb&category=GPU&gpu=RTX%203080,RTX%203070,RTX%203090&manufacturer=NVIDIA&manufacturer_filter=NVIDIA~3,ASUS~11,EVGA~4,GIGABYTE~11,MSI~6,PALIT~6,PNY~4,ZOTAC~6"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


def test_interval(interval):
    for i in range(50):
        r = requests.get(url, headers=headers)
        if r.status_code != 200 or json.loads(r.content).get("searchedProducts") is None:
            print(f"Banned on {interval}, iteration {i}")
            return False
        print(f"Testing interval: {interval}s..., iteration: {i}")
        time.sleep(interval)
    return True

intervals = [30, 15, 10, 5]
for interval in intervals:
    test_interval(interval)
