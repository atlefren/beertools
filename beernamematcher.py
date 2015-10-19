# -*- coding: utf-8 -*-
import Levenshtein

BEER_TYPES = [
    u'imperial',
    u'porter',
    u'stout',
    u'coffee',
    u'wheat',
    u'india',
    u'hefeweizen',
    u'barleywine',
    u'barrel-Aged',
    u'red',
    u'ale',
    u'double',
    u'ipa',
    u'trappistes',
    u'amber',
    u'berliner',
    u'weisse',
    u'pale',
    u'pilsner',
    u'blonde',
    u'dipa',
    u'rye',
    u'tripel',
    u'weissbier',
    u'wit',
    u'saison',

]

AND_WORDS = [
    u'og',
    u'and'
]


class BeerNameMatcher(object):

    def __init__(self, brewery_name, beer_list):
        self.brewery_name = unicode(brewery_name)
        self.beer_list = self._prepare(beer_list)

    def match_name(self, name):
        name = self._lower_strip(name)
        match = self._match_on(name, 'name')
        if match:
            return match

        name = self._remove_brewery_name(name)
        match2 = self._match_on(name, 'cleaned')
        if match2:
            return match2

        name = self._remove_type(name)
        match3 = self._match_on(name, 'name_no_type')
        if match3:
            return match3

        return None

    def _match_on(self, name, property_name):
        with_dist = [self._get_distance(name, beer_obj, property_name)
                     for beer_obj in self.beer_list]

        if len(with_dist) == 0:
            return
        highest = max(with_dist, key=lambda x: x['dist'])
        # print highest['dist']
        if highest['dist'] > 0.7:
            return highest['beer']

    def _get_distance(self, name, beer_obj, property_name):
        name2 = beer_obj[property_name]
        # print name, name2
        return {
            'beer': beer_obj['beer_obj'],
            'dist': Levenshtein.ratio(unicode(name), unicode(name2))
        }

    def _prepare(self, beer_list):
        return [self._clean(beer) for beer in beer_list]

    def _remove_type(self, name):
        name_fixed = []
        for word in name.split():
            if word not in BEER_TYPES:
                name_fixed.append(word)
        return ' '.join(name_fixed)

    def _remove_brewery_name(self, name):
        return name.replace(self.brewery_name.lower(), '')

    def _lower_strip(self, name):
        name = unicode(name.lower().strip())
        name_fixed = []
        for word in name.split():
            if word in AND_WORDS:
                name_fixed.append(u'&')
            else:
                name_fixed.append(word)
        return ' '.join(name_fixed)

    def _clean(self, beer):
        name = self._lower_strip(beer['name'])
        name_cleaned = self._remove_brewery_name(name)
        return {
            'beer_obj': beer,
            'cleaned': name_cleaned,
            'name': name,
            'name_no_type': self._remove_type(name_cleaned)
        }
