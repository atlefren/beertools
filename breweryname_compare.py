# -*- coding: utf-8 -*-
import json
from brewerynamematcher import BreweryNameMatcher
from beernamematcher import BeerNameMatcher


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


def get_beers(beer_list, brewery_name, attr_name):
    return [beer for beer in beer_list if beer[attr_name] == brewery_name]


def compare_beers(pol_data, rb_data):
    breweries_pol = get_breweries(pol_data, 'Produsent')
    breweries_rb = wrap_breweries(get_breweries(rb_data, 'brewery'))

    with open('data/beer_nomatch.txt', 'w') as nomatch:
        brewery_matcher = BreweryNameMatcher(breweries_rb)
        for brewery in breweries_pol:
            match = brewery_matcher.match_name(brewery)
            if match is not None:
                rb_beers = get_beers(rb_data, match['name'], 'brewery')
                beer_matcher = BeerNameMatcher(match['name'], rb_beers)

                nomatch.write(match['name'].encode('utf8') + '\n')
                pol_beers = get_beers(pol_data, brewery, 'Produsent')
                for pol_beer in pol_beers:
                    beer_match = beer_matcher.match_name(pol_beer['Varenavn'])
                    if not beer_match:
                        string = '\t%s ' % pol_beer['Varenavn']
                        nomatch.write(string.encode('utf8') + '\n')

if __name__ == '__main__':

    pol_data = read_json('data/polet.json')
    rb_breweries = read_json('data/rb_breweries.json')
    compare_breweries(pol_data, rb_breweries)
