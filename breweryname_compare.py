# -*- coding: utf-8 -*-
import json
from beertools import BreweryNameMatcher


def read_json(filename):
    with open(filename, 'r') as infile:
        return json.loads(infile.read())


def get_breweries_polet():
    with open('data/polet.json', 'r') as infile:
        data = json.loads(infile.read())

        breweries = list(set([product['Produsent'] for product in data]))
        return sorted(breweries), data


def get_breweries(beer_list, property_name):
    return sorted(list(set([beer[property_name] for beer in beer_list])))


def get_breweries_ratebeer():
    with open('data/ratebeer.json', 'r') as infile:
        data = json.loads(infile.read())
        breweries = list(set([product['brewery'] for product in data]))
        return sorted(breweries)


def wrap_breweries(breweries):
    return [{'id': index, 'name': brewery}
            for index, brewery in enumerate(breweries)]


def compare_breweries(pol_data, breweries_rb):
    breweries_pol = get_breweries(pol_data, 'Produsent')
    # breweries_rb = wrap_breweries(get_breweries(rb_data, 'brewery'))
    matcher = BreweryNameMatcher(breweries_rb)

    with open('data/nomatch.txt', 'w') as nomatch:
        with open('data/match.txt', 'w') as match_file:
            for brewery in breweries_pol:
                match = matcher.match_name(brewery)
                if match is None:
                    nomatch.write(brewery.encode('utf8') + '\n')
                else:
                    string = '%s: %s' % (brewery, match['name'])
                    match_file.write(string.encode('utf8') + '\n')


def compare_breweries_geojson(breweries, breweries_rb):
    breweries_rb = [b for b in breweries_rb if b['country'] == 154]
    matcher = BreweryNameMatcher(breweries_rb)

    for brewery in breweries['features']:
        brewery_name = brewery['properties']['name']
        match = matcher.match_name(brewery_name)
        if match is not None:
            brewery['properties']['ratebeer_id'] = match['id']
    return breweries


if __name__ == '__main__':

    pol_data = read_json('data/polet.json')
    # breweries = read_json('data/breweries.geojson')
    rb_breweries = read_json('data/rb_breweries.json')
    compare_breweries(pol_data, rb_breweries)

    '''
    res = compare_breweries_geojson(breweries, rb_breweries)
    with open('data/breweries_matched.geojson', 'w') as outfile:
        outfile.write(json.dumps(res, indent=4))
    '''
