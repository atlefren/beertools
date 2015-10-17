# -*- coding: utf-8 -*-
import json
from brewerynamematcher import match_name


def get_breweries_polet():
    with open('data/polet.json', 'r') as infile:
        data = json.loads(infile.read())

        breweries = list(set([product['Produsent'] for product in data]))
        return sorted(breweries)


def get_breweries_ratebeer():
    with open('data/ratebeer.json', 'r') as infile:
        data = json.loads(infile.read())

        breweries = list(set([product['brewery'] for product in data]))
        return sorted(breweries)


def wrap_breweries(breweries):
    return [{'id': index, 'name': brewery}
            for index, brewery in enumerate(breweries)]


if __name__ == '__main__':

    breweries_polet = get_breweries_polet()

    breweries_ratebeer = wrap_breweries(get_breweries_ratebeer())

    with open('data/nomatch.txt', 'w') as nomatch:

        for brewery in breweries_polet:
            match = match_name(brewery, breweries_ratebeer)
            if match is None:
                nomatch.write(brewery.encode('utf8') + '\n')
