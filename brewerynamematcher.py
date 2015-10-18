# -*- coding: utf-8 -*-
import re
import Levenshtein
import string
import json

COMMON_BREWERY_TERMS = [
    u'Trappistenbrouwerij',
    u'Trappistenbier-Brauerei',
    u'Bierbrouwerij',
    u'Bryggeri & Spiseri',
    u'Mikrobryggeri',
    u'Microbirrificio',
    u'Ølbryggeri',
    u'Bryggerhuset',
    u'Bryggerier',
    u'Bryggeriet',
    u'Bryggeri',
    u'Old Brewery',
    u'Brewery Company',
    u'Brewing Company',
    u'Brewery',
    u'Breweries',
    u'Brewing Co',
    u'Craft Beer',
    u'Brewing',
    u'Cervezas',
    u'Panimo',
    u'Picobrouwerij',
    u'Microbrouwerij',
    u'Kleinbrouwerij',
    u'Kleinbrauerei',
    u'Ölgerð',
    u'Brouw.',
    u'Brauerei',
    u'Brouwerij',
    u'Brygghus',
    u'Bryghus',
    u'Birra',
    u'Brasserie Artisanale',
    u'Brasserie',
    u'Brasserie',
    u'Brasseries',
    u'Bieres',
    u'Pivovary',
    u'Pivovar',
    u'Beer co',
    u'Ale',
    u'Beer',
    u'Weissbräu'
]

STOPWORDS = [
    u'sa',
    u'la',
    u'le',
    u'de',
    u'as',
    u'ab',
    u'the',
    u'ltd',
    u's.r.l.',
    u'sprl',
    u'GmbH'
]


def remove_stopwords(name):
    return ' '.join([word for word in name.split() if word not in STOPWORDS])


def remove_corporation(name):
    if name.endswith(')'):
        return re.sub('\(.+?\)', '', name).strip()
    return name


def remove_common(name):
    for common in COMMON_BREWERY_TERMS:
        name = name.replace(common.lower(), '').strip()
    return name


def clean(name):
    return name.lower().strip()


def remove_collab(name):
    index = name.find('/')
    if index > -1:
        return name[:index]
    index2 = name.find('\\')
    if index2 > -1:
        return name[:index2]
    return name


def strip_punctuation(name):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    return re.sub("\s\s+", " ", regex.sub(' ', name))


def read_json(filename):
    with open(filename, 'r') as infile:
        return json.loads(infile.read())

known_misspellings = read_json('brewery_misspellings.json')


class BreweryNameMatcher(object):

    def __init__(self, brewery_list):
        self.misspellings = known_misspellings
        self.brewery_list = self._prepare_list(brewery_list)

    def match_name(self, name):
        name = self._normalize_name(unicode(name))
        if name == '':
            return None

        match = self._compare(name, 0.95)
        if match is not None:
            return match

        name = remove_common(name)
        match = self._compare(name, 0.8, remove_common)
        if match is not None:
            return match

        match = self._count_matches(name)
        if match is not None:
            return match
        return None

    def _normalize_name(self, name):
        name = self._fix_misspelling(name)
        return remove_corporation(remove_collab(remove_stopwords(clean(name))))

    def _prepare_list(self, brewery_list):
        result = []
        for brewery in brewery_list:
            obj = {
                'brewery': brewery,
                'normalized': self._normalize_name(brewery['name'])
            }
            result.append(obj)
        return result

    def _fix_misspelling(self, name):
        for misspelling in self.misspellings:
            if name in misspelling['misspellings']:
                return misspelling['name']
        return name

    def _get_distance(self, name, brewery_obj, operation=None):

        name2 = brewery_obj['normalized']
        if operation is not None:
            if operation.__name__ not in brewery_obj:
                brewery_obj[operation.__name__] = operation(name2)
            name2 = brewery_obj[operation.__name__]
        return {
            'brewery': brewery_obj['brewery'],
            'dist': Levenshtein.ratio(unicode(name), unicode(name2))
        }

    def _compare(self, name, threshold, operation=None):
        with_dist = [self._get_distance(name, brewery_obj, operation)
                     for brewery_obj in self.brewery_list]

        highest = max(with_dist, key=lambda x: x['dist'])
        if highest['dist'] > threshold:
            return highest['brewery']
        return None

    def _check_word_similarity(self, name, brewery_obj):
        count = 0
        for word in name:
            if 'split_words' not in brewery_obj:
                brewery_obj['split_words'] = strip_punctuation(
                    brewery_obj['normalized']
                ).split(' ')
            split_words = brewery_obj['split_words']
            for word2 in split_words:
                if word not in [u'gmbh', u'group', u'united'] and len(word) > 3 and word == word2:
                    count = count + 1
        return {
            'brewery': brewery_obj['brewery'],
            'count': count
        }

    def _count_matches(self, name):
        name = strip_punctuation(name).split(' ')

        with_count = [self._check_word_similarity(name, brewery_obj)
                      for brewery_obj in self.brewery_list]
        closest = max(with_count, key=lambda x: x['count'])

        if closest['count'] > 0:
            return closest['brewery']
