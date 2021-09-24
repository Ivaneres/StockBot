import yaml

from data.api_parser import APIParser, JSONSelector


def load_source(path: str) -> APIParser:
    with open(path, "r") as fp:
        data = yaml.safe_load(fp.read())
    selectors = [
        JSONSelector(
            prod_path=x["products_path"],
            name_path=x["name_path"],
            stock_status_path=x["status_path"],
            stock_status_message=x["stock_message"],
            price_path=x.get("price_path")
        ) for x in data["selectors"]
    ]
    return APIParser(
        request_url=data["url"],
        headers=data.get("headers"),
        selectors=selectors
    )
