import io
import operator
from functools import reduce

import requests as requests


def lookup(data, keys):
    return reduce(operator.getitem, keys, data)


def create_image(url: str) -> io.BytesIO:
    img_r = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    })
    if img_r.status_code != 200:
        raise ConnectionError(f"Failed to fetch image, response code {img_r.status_code}")
    img_bytes = img_r.content
    img = io.BytesIO()
    img.write(img_bytes)
    img.seek(0)
    return img
