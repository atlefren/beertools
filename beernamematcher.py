# -*- coding: utf-8 -*-
import re

import Levenshtein

from brewerynamematcher import strip_punctuation

BEER_TYPES = [
    u'Imperial Wheat Stout',
    u'Imperial Stout',
    u'Milk Stout',
    u'White IPA',
    u'Saison IPA',
    u'Rye IPA',
    u'Session IPA',
    u'Dobbel IPA',
    u'Black IPA',
    u'DIPA',
    u'IPA',
    u'APA',
    u'Belgian Tripel',
    u'Farmhouse Ale',
    u'India Pale Ale',
    u'India Dark Ale',
    u'Brown Ale',
    u'Belgian Ale',
    u'Pale Ale',
    u'Amber Ale',
    u'Blonde Ale',
    u'Dubbel Bruin',
    u'Blond',
    u'Geuze',
    u'Saison',
    u'Witbier',
    u'Wit',
    u'Lager',
    u'Cream Stout',
    u'Trappistes',
    u'Trappist',
]

BEER_TYPES = [x.lower() for x in BEER_TYPES]

AND_WORDS = [
    u'og',
    u'and'
]

PACKAGE_TYPES = [
    u' (cask)',
    u' (bottle)',
    u' (bottle/keg)',
    u' (bottle / keg)',
    u' (cask & bottle conditioned)',
    u' (pasteurized)',
    u' (pasteurised)',
    u' (filtered)',
]


def lower_strip(name):
    name = unicode(name.lower().strip())
    name_fixed = []
    for word in name.split():
        if word in AND_WORDS:
            name_fixed.append(u'&')
        else:
            name_fixed.append(word)
    return ' '.join(name_fixed)


def remove_punctuation2(name):
    return strip_punctuation(name).replace('(', '').replace(')', '').replace('/', '')


def remove_type(name):
    for beer_type in BEER_TYPES:
        if beer_type in name:
            name = name.replace(beer_type, '')
    return name.strip()


def remove_numbers(name):
    return filter(lambda x: not x.isdigit(), name)


def split_parens(name):
    r3 = re.compile("(.*?)\s*\((.*?)\)")
    m3 = r3.match(name)
    if m3:
        return [m3.group(1), m3.group(2)]
    return [name]


def remove_packaging(name):
    for packaging in PACKAGE_TYPES:
        if packaging in name:
            name = name.replace(packaging, '')
    return name


def find_bottle_version(beers):
    wanted = ['(bottle)', '(bottle/keg)', '(cask & bottle conditioned)',
              '(pasteurized)', '(pasteurised)', '(filtered)', '(bottle / keg)']
    for b in beers:
        if type(b) is dict:
            beer = b['beer']
        else:
            beer = b
        n = beer.operations['lower_strip']

        for p in wanted:
            if p in n:
                return b
    return beers[0]


class Beer(object):

    def __init__(self, beer):
        self.operations = {}
        self.last_name = beer['name']
        self.beer = beer

    def get_operation(self, operation):
        if operation.__name__ not in self.operations:
            self.last_name = operation(self.last_name)
            self.operations[operation.__name__] = self.last_name
        return self.operations[operation.__name__]


class BeerNameMatcher(object):

    def __init__(self, brewery_name, beer_list):
        self.brewery_name = unicode(brewery_name)
        self.beer_list = self._prepare(beer_list)

    def match_name(self, name):
        org_name = name

        def remove_brewery_name(beer_name):
            brewery_name = self.brewery_name.lower()
            return beer_name.replace(brewery_name, '')

        def remove_brewery_name_parts(beer_name):
            brewery_name = self.brewery_name.lower()
            for part in brewery_name.split(' '):
                beer_name = beer_name.replace(part, ' ')
            return beer_name

        operations = [lower_strip, remove_brewery_name, remove_brewery_name_parts,
                      remove_packaging, remove_punctuation2, remove_type]

        for operation in operations:
            match, name = self._check_match(name, operation)
            if match:
                return match

        match = self._check_split(remove_brewery_name_parts(lower_strip(org_name)))

        if match:
            return match
        return None

    def _check_match(self, name1, operation):
        # print operation.__name__
        name1 = operation(name1)

        with_dist = [self._get_distance(name1, beer.get_operation(operation), beer)
                     for beer in self.beer_list]

        if len(with_dist) == 0:
            return

        max_score = max(x['dist'] for x in with_dist)
        highest = [beer for beer in with_dist if beer['dist'] == max_score]
        if len(highest) == 1:
            highest = highest[0]
        else:
            highest = find_bottle_version(highest)

        match = None
        if highest['dist'] > 0.9:
            match = highest['beer'].beer
        return match, name1

    def _check_split(self, name1):
        match = []
        score = 0
        for part in remove_type(name1).split('/'):
            for beer in self.beer_list:
                split2 = remove_type(beer.operations['remove_packaging'])
                for part2 in split2.split('/'):
                    part = remove_numbers(part)
                    part2 = remove_numbers(part2)

                    dist = Levenshtein.ratio(unicode(part), unicode(part2))
                    if dist > score:
                        score = dist
                        match = [beer]
                    elif dist == score:
                        match.append(beer)

        if score > 0.7:
            return find_bottle_version(match).beer

        for p1 in split_parens(remove_type(remove_numbers(name1))):
            for beer in self.beer_list:
                for p2 in split_parens(remove_numbers(beer.operations['remove_packaging'])):
                    dist = Levenshtein.ratio(unicode(p1), unicode(p2))
                    if dist > score:
                        score = dist
                        match = [beer]
                    if dist == score:
                        match.append(beer)
        if score > 0.7:
            return find_bottle_version(match).beer

        for p1 in remove_type(remove_numbers(name1)).split(' '):
            for beer in self.beer_list:
                for p2 in remove_numbers(beer.operations['remove_packaging']).split(' '):
                    dist = Levenshtein.ratio(unicode(p1), unicode(p2))
                    if dist > score:
                        score = dist
                        match = [beer]
                    if dist == score:
                        match.append(beer)
        if score > 0.7:
            return find_bottle_version(match).beer

    def _get_distance(self, name1, name2, beer):
        dist = Levenshtein.ratio(unicode(name1), unicode(name2))
       # print '%s | %s (%s)' % (name1, name2, dist)
        return {
            'beer': beer,
            'dist': dist
        }

    def _prepare(self, beer_list):
        return [Beer(beer) for beer in beer_list]
