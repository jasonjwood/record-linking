import json
import time

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
        # todo: I feel like this is unnecessary; figure out how to eliminate it.
        return "{\"product_name\": \"" + self.product_name + "\", \"listings\": " + json.dumps(self.listings) + "}"

    def to_eval_json(self):
        s = ""
        for listing in self.listings:
            s += "{" + self.product_name + "} = {" + listing['title'] + "}\n"

        s += "\n\n"
        return s



class Match:
    product = None
    listing = None

    def __init__(self, product, listing):
        self.product = product
        self.listing = listing


def main():
    start = time.time()

    # Fetch products, lower case all values, store in dict by manufacturer
    products_dict = dict()
    with open("products.txt") as products_file:
        for line in products_file:
            product = json.loads(line)
            product['manufacturer'] = product['manufacturer'].lower()
            product['model'] = product['model'].lower()
            if product.get('family', None) is not None:
                product['family'] = product['family'].lower()

            if product['manufacturer'] in products_dict:
                products_dict[product['manufacturer']].append(product)
            else:
                products_dict[product['manufacturer']] = [product]

    print "1 >> " + str(time.time() - start)

    # Create Output
    results_dict = dict()

    # Match listings to products to form results
    match_time = 0
    with open("listings.txt") as listings_file:
        for line in listings_file:
            # Load listing
            listing = json.loads(line)

            # Match listing to products
            match_start_time = time.time()
            match = match_listing_to_product(listing, products_dict)
            match_time += time.time() - match_start_time

            # Add match (if found) to the results list
            if match is None:
                continue

            match_product_name = match.product['product_name']
            if match_product_name not in results_dict:
                results_dict[match_product_name] = Result(match_product_name, [])

            results_dict[match_product_name].listings.append(listing)

    print "match_time = " + str(match_time)
    print "2 >> " + str(time.time() - start)

    # Write results file
    listing_count = 0
    with open("results.txt", "w") as results_file:
        for key in results_dict:
            results_file.writelines([results_dict[key].to_json(), "\n"])
            listing_count += len(results_dict[key].listings)

    # Write evaluation file
    with open("eval.txt", "w") as eval_file:
       for key in results_dict:
           eval_file.writelines([results_dict[key].to_eval_json().encode('utf8')])

    print "# matches = " + str(len(results_dict))
    print "# listings = " + str(listing_count)
    print "Run time = " + str(time.time() - start) + " seconds"


def match_listing_to_product(listing, products):
    # For now, naively assume that we just want to match manufacturer and find "family" and "model" in the listing title
    listing_manuf = listing['manufacturer'].lower()
    if products.get(listing_manuf, None) is None:
        return None

    tokens = set()
    for token in listing['title'].split():
        tokens.add(token.lower())

    # Dirty hack that's probably not appropriate in the general case - from inspection of the data, when we see "for",
    # we're often looking at an accessory rather than a camera
    if "for" in tokens or "pour" in tokens:
        return None

    for product in products[listing_manuf]:
        if product['model'] in tokens and (product.get('family', None) is None or product['family'] in tokens):
            return Match(product, listing)

    return None

main()
print "Done"
