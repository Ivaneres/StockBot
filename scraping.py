from nvidia import *

parsers = [NvidiaParser()]
all_products = []

for parser in parsers:
    parser.get_product_data()
    parser.check_stock()
    all_products += parser.product_list
    
for product in all_products:
    if product.in_stock:
        print(product.name + ": in stock. Source: " + product.source)