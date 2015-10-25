# -*- coding: utf-8 -*-

from util import read_json


def get_beers(beer_list, brewery_name, attr_name):
    return [beer for beer in beer_list if beer[attr_name] == brewery_name]

polet_beers = read_json('data/polet.json')


with open('data/feil_til_polet.txt', 'r') as infile:
    for line in infile.readlines():
        split = line.replace('\n', '').split(':')
        pol_name = split[0]

        beers = get_beers(polet_beers, pol_name, 'Produsent')
        if len(beers):
            print pol_name
            print '=' * len(pol_name)
            print '\n'
            print 'Produsent: %s' % pol_name
            print 'Burde være: %s' % split[1]
            print '\n'
            print 'Gjelder:'
            for beer in beers:
                print '%s (%s)' % (beer['Varenavn'], beer['Varenummer'])
            print '\n'
