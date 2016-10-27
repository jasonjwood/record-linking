import json
import time
from collections import defaultdict


# Given list of products and list of listings of products, match listings to products
# (It's more important to have a correct match than to identify all matches.)
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
    results_dict = defaultdict(list)

    # Match listings to products to form results
    match_time = 0
    with open("listings.txt") as listings_file:
        for line in listings_file:
            # Load listing
            listing = json.loads(line)

            # Match listing to products
            match_start_time = time.time()
            product_name = match_listing_to_product(listing, products_dict)
            match_time += time.time() - match_start_time

            # Add match (if found) to the results list
            if product_name is None:
                continue

            results_dict[product_name].append(listing)

    print "match_time = " + str(match_time)
    print "2 >> " + str(time.time() - start)

    # Write results file
    listing_count = 0
    with open("results.txt", "w") as results_file:
        for key in results_dict:
            results_file.write(
                    "{\"product_name\": \"" + key + "\", \"listings\": " + json.dumps(results_dict[key]) + "}\n")
            listing_count += len(results_dict[key])

    # Write evaluation file
    with open("eval.txt", "w") as eval_file:
        for key in results_dict:
            s = "".join(["{" + key + "} = {" + listing['title'] + "}\n" for listing in results_dict[key]]) + "\n\n"
            eval_file.write(s.encode('utf8'))

    print "# matches = " + str(len(results_dict))
    print "# listings = " + str(listing_count)
    print "Run time = " + str(time.time() - start) + " seconds"


# Return the name of the product that matches the given listing.
# For now, naively assume that we just want to match manufacturer and find "family" and "model" in the listing title
def match_listing_to_product(listing, products):
    # manufacturer must match
    products_by_manufacturer = products.get(listing['manufacturer'].lower(), None)
    if products_by_manufacturer is None:
        return None

    # tokenize listing title and look for key elements of product
    tokens = set([token.lower() for token in listing['title'].split()])

    # Dirty hack that's probably not appropriate in the general case - from inspection of the data, when we see "for"
    # we're often looking at an accessory rather than a camera - We lose ~40 good matches to eliminate ~20 bad matches
    if "for" in tokens or "pour" in tokens:
        return None

    for product in products_by_manufacturer:
        if product['model'] in tokens and (product.get('family', None) is None or product['family'] in tokens):
            return product['product_name']

    return None

main()
print "Done"
