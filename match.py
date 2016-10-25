import json

# Given list of products and list of listings of products, match listings to products
# (It's more important to have a correct match than to identify all matches.)

# Start naive, then get more efficient



class Result:
    product_name = ''
    listings = []

    def __init__(self, name, listings):
        self.listings = listings
        self.product_name = name


class Match:
    product = None
    listing = None

    def __init__(self, product, listing):
        self.product = product
        self.listing = listing



def main():
    # Fetch products
    products_list = []
    with open("products.txt") as products_file:
        for line in products_file:
            product = json.loads(line)
            print product
            product['product_name'] = product['product_name'].replace("_", " ")
            products_list.append(product)

    # Create Output
    results_list = set()

    # Match listings to products to form results
    with open("listings.txt") as listings_file:
        for line in listings_file:
            listing = json.loads(line)
            # naively for now, assume that we have a match if:
            #   product.manufacturer=listing.manufacturer
            #   product.model and product.family (if exists) are exact-matched in listing title

            match = match_listing_to_product(listing, products_list)
            if match is not None:
                results_list(match.product_name).append(listing)
                # todo: ensure no dupes in list


def match_listing_to_product(listing, products):
    for product in products:
        if product['manufacturer'] == listing['manufacturer']:
            tokens = listing['title'].split()
            if tokens.contains(product.model):
                if product['family_name'] is None or tokens.contains(product['family_name']):
                    return Match(product, listing)

    return None







main()