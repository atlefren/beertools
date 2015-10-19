# -*- coding: utf-8 -*-
import json
from collections import defaultdict

from brewerynamematcher import BreweryNameMatcher
from beernamematcher import BeerNameMatcher
from util import read_json


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


def get_beers(beer_list, brewery_name, attr_name):
    return [beer for beer in beer_list if beer[attr_name] == brewery_name]


def find_in_list(dicts, key, value):
    return (item for item in dicts if item[key] == value).next()


def findall_in_list(dicts, key, value):
    return [item for item in dicts if item[key] == value]


def compare_beers(pol_data, rb_beers, breweries_rb):
    breweries_pol = get_breweries(pol_data, 'Produsent')

    grouped = defaultdict(list)

    brewery_matcher = BreweryNameMatcher(breweries_rb)
    for brewery_pol in breweries_pol:
        match = brewery_matcher.match_name(brewery_pol)
        if match is not None:
            grouped[match['id']].append(brewery_pol)

    with open('data/beer_nomatch.txt', 'w') as nomatch:
        with open('data/beer_match.txt', 'w') as match:
            for key, value in grouped.iteritems():
                rb_brewery = find_in_list(breweries_rb, 'id', key)['name']
                rb_beers_for_brewery = findall_in_list(rb_beers, 'brewery_id', key)

                beer_matcher = BeerNameMatcher(rb_brewery, rb_beers_for_brewery)

                nomatch.write(rb_brewery.encode('utf8') + '\n')
                match.write(rb_brewery.encode('utf8') + '\n')
                for pol_brewery in value:
                    line = '\t %s' % pol_brewery
                    nomatch.write(line.encode('utf8') + '\n')
                    match.write(line.encode('utf8') + '\n')
                    pol_beers = findall_in_list(pol_data, 'Produsent', pol_brewery)
                    for pol_beer in pol_beers:
                        pol_beer_name = pol_beer['Varenavn']
                        beer_match = beer_matcher.match_name(pol_beer_name)
                        if beer_match is None:
                            line2 = '\t\t %s' % pol_beer_name
                            nomatch.write(line2.encode('utf8') + '\n')
                        else:
                            line2 = '\t\t %s - %s' % (pol_beer_name, beer_match['name'])
                            match.write(line2.encode('utf8') + '\n')


'''
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
'''
if __name__ == '__main__':

    pol_data = read_json('data/polet.json')
    rb_beers = read_json('data/rb_beers.json')
    rb_breweries = read_json('data/rb_breweries.json')

    compare_beers(pol_data, rb_beers, rb_breweries)
