indexer = Indexer(
    WebScrapeSource(
        query_formatter=lambda x: f"https://nyaa.si/?f=1&c=1_2&q={x.replace(' ', '+')}&s=seeders&o=desc",
        scraper=Scraper(
            parser="lxml",
            root=("div", ["success", "default"]),
            subelem_selectors=[
                SubelementSelector([("td", 1), ("a", [], -1)], attribute="text"),
                SubelementSelector([("td", ["text-center"], 0), ("a", [])], attribute="href"),
                SubelementSelector([("td", ["text-center"], 3)], attribute="text"),
                SubelementSelector([("td", ["text-center"], 1)], attribute="text")
            ],
            postprocess=lambda x: [(y[0], "https://nyaa.si" + y[1], y[2], y[3]) for y in x]
        )
    )
)
