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

    def to_json(self):
        return "{\"product_name\": \"" +  self.product_name + "\", \"listings\": " + json.dumps(self.listings) + "}"


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
            product['original_name'] = product['product_name']
            product['product_name'] = product['product_name'].replace("_", " ")
            products_list.append(product)

    # Create Output
    results_list = dict()

    # Match listings to products to form results
    with open("listings.txt") as listings_file:
        for line in listings_file:
            listing = json.loads(line)
            # naively for now, assume that we have a match if:
            #   product.manufacturer=listing.manufacturer
            #   product.model and product.family (if exists) are exact-matched in listing title

            match = match_listing_to_product(listing, products_list)
            if match is not None:
                match_product_name = match.product['original_name']
                if match_product_name not in results_list:
                    results_list[match_product_name] = Result(match_product_name, [])

                results_list[match_product_name].listings.append(listing)

                # todo: ensure no dupes in list
    #print results_list.__sizeof__()
    #for result in results_list:
    #    print result

    with open("results.txt", "w") as results_file:
        for key in results_list:
            results_file.writelines([results_list[key].to_json(), "\n"])



def match_listing_to_product(listing, products):
    for product in products:
        if product['manufacturer'] == listing['manufacturer']:
            tokens = set()
            for token in listing['title'].split():
                tokens.add(token)

            if product['model'] in tokens:
                if product.get('family', None) is None or product['family'] in tokens:
                    return Match(product, listing)

    return None







main()

print "Done"