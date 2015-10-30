# -*- coding: utf-8 -*-

import re

import Levenshtein

from brewerynamematcher import strip_punctuation

BEER_TYPES = [
    u'Imperial Wheat Stout',
    u'American Pale Ale',
    u'Imperial Coffee Stout',
    u'Imperial Stout',
    u'Imperial IPA',
    u'Barleywine',
    u'Imperial Black IPA',
    u'Milk Stout',
    u'White IPA',
    u'Saison IPA',
    u'Rye IPA',
    u'Session IPA',
    u'Dobbel IPA',
    u'Double IPA',
    u'Black IPA',
    u'DIPA',
    u'IPA',
    u'APA',
    u'Belgian Tripel',
    u'Farmhouse Ale',
    u'India Pale Ale',
    u'India Red Ale',
    u'Indian Pale Ale',
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
    u'Craft Lager',
    u'Premium Lager',
    u'Lager',
    u'Cream Stout',
    u'Trappistenbier',
    u'Trappistes',
    u'Trappist',
    u'Stout Porter',
    u'Imperial Porter',
    u'London Porter',
    u'Porter',
    u'Hefe-Weizen',
    u'Hefeweizen',
    u'Wheat Beer',
    u'Pilsner',
    u'Pils',
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

WANTED_PACKAGE_TYPES = [
    u' (bottle)',
    u' (bottle/keg)',
    u' (bottle / keg)',
    u' (bottle/can)',
    u' (cask & bottle conditioned)',
    u' (pasteurized)',
    u' (pasteurised)',
    u' (filtered)',
]

UNWANTED_PACKAGE_TYPES = [
    u'cask'
]

COMMON_WORDS2 = [
    u'Brewers Reserve',
    u'Brewery',
    u'Barrel-Aged',
    u'Single Hopped',
    u'originalen',
    u'unfiltered',
    u'brewing',
    u'Brasserie',
    u'project',
    u'Økologisk',
    u'Single Hop'
]

DUPLICATES = {
    'red': ['rouge'],
    'unfiltered': ['non filtrata'],
    'lager': ['lager / pilsner'],
    'extra': ['ekstra'],
    'brown': ['brune', 'bruin']
}


def remove_multiple_spaces(s):
    return ' '.join(s.split())


def remove_from_str(s, remove):
    return remove_multiple_spaces(s.replace(remove, '').strip())


def remove_from_str_parts(s, remove):

    remove_words = remove.lower().split(' ')
    combined = []
    for word in s.split(' '):
        if word not in remove_words:
            combined.append(word)
    return ' '.join(combined).strip()


def lower_strip2(s):
    s = s.lower().strip()
    return ' '.join(s.split())


def fix_typography(name):
    name = name.replace('\'', u'’').replace('\'', u'`')
    p = re.compile('([a-z])/([a-z])')
    return p.sub(r'\1 / \2', name)


def remove_packaging2(name):
    for packaging in WANTED_PACKAGE_TYPES:
        if packaging in name:
            name = name.replace(packaging, '').strip()
    return name


def remove_size2(name):
    return re.sub(r'(\d{1,4} cl)', '', name).strip()


def remove_abv2(name):
    name = re.sub(r'(\(\d+(\.\d{1,2})?\s*%\))', '', name).strip()
    return re.sub(r'(\d{1,2}\.?\d{0,4}\s*%)', '', name).strip()


def remove_year2(name):
    return re.sub(r'(\(\d{4}\s*-\s*(\d{4})?\))', '', name).strip()


def fix_and_words(name):
    name_fixed = []
    for word in name.split():
        if word in AND_WORDS:
            name_fixed.append(u'&')
        else:
            name_fixed.append(word)
    return ' '.join(name_fixed).strip()


def remove_words(s, words):
    s = s.lower()
    for word in words:
        word = word.lower()
        if word in s:
            s = re.sub('(?i)' + re.escape(word), '', s)
    return remove_multiple_spaces(s.strip())


def remove_type2(name):
    return remove_words(name, BEER_TYPES)


def remove_common2(name):
    return remove_words(name, COMMON_WORDS2)


def remove_punctuation3(name):
    return strip_punctuation(name) \
        .replace('(', '') \
        .replace(')', '') \
        .replace('/', '') \
        .strip()


def remove_single_year(name):
    return re.sub(r'(19|20)\d{2}', '', name).strip()


def unique_list(l, l2):
    ulist = []
    for x in l:
        if x in ulist:
            if x not in l2:
                ulist.append(x)
        else:
            ulist.append(x)
    return ulist


def remove_duplicates(name):
    name = ' %s ' % name
    for word, duplicates in DUPLICATES.iteritems():
        for duplicate in duplicates:
            regex = '(?<![a-z])(%s)(?![a-z])' % duplicate
            p = re.compile(regex)
            name = p.sub(word, name)
    name = name.strip().split()
    return ' '.join(unique_list(name, DUPLICATES.keys()))


def shift_range(value):
    return (((value - 0.0) * (100.0 - 90.0)) / (100.0 - 0.0)) + 90.0


def remove_collab(name):
    if '/' in name and name.index('/') < len(name) / 2.0:
        name_last = name[name.index('/') + 1:].strip()
        name = ' '.join(name_last.split()[1:])
    return name


def is_substring_of(s1, s2):
    return s1 in s2


def num_words(s):
    return len(s.split())


def sort_words(s):
    return ' '.join(sorted(s.split()))


def ratio(s1, s2, brewery_name):
    s1 = unicode(s1)
    s2 = unicode(s2)
    brewery_name = brewery_name.lower()

    def remove_brewery(name):
        return remove_from_str(name, brewery_name)

    def remove_brewery_parts(name):
        return remove_from_str_parts(name, brewery_name)

    operations = [
        {'func': lower_strip2, 'threshold': 0.95},
        {'func': fix_typography, 'threshold': 0.95},
        {'func': remove_brewery, 'threshold': 0.95},
        {'func': remove_collab, 'threshold': 0.95},
        {'func': remove_brewery_parts, 'threshold': 0.95},
        {'func': remove_packaging2, 'threshold': 0.95},
        {'func': fix_and_words, 'threshold': 0.95},
        {'func': remove_duplicates, 'threshold': 0.95},
        {'func': remove_abv2, 'threshold': 0.95},
        {'func': remove_year2, 'threshold': 0.95},
        {'func': remove_size2, 'threshold': 0.95},
        {'func': remove_punctuation3, 'threshold': 0.95},
        {'func': sort_words, 'threshold': 0.95, 'restore': True},
        {'func': remove_common2, 'threshold': 0.95},
        {'func': remove_type2, 'threshold': 0.8},
        {'func': remove_single_year, 'threshold': 0.95}
    ]
    length = len(operations)
    for index, operation in enumerate(operations):
        restore = operation.get('restore', False)

        s1_tmp = operation['func'](s1)
        s2_tmp = operation['func'](s2)

        if s1 == s1_tmp and s2 == s2_tmp:
            c = 1
        else:
            c = shift_range(float(length - index) / float(length) * float(100)) / 100.0
        dist = Levenshtein.ratio(unicode(s1_tmp), unicode(s2_tmp)) * c

        if s1_tmp == '' and s2_tmp == '':
            dist = 0.0

        #print operation['func'].__name__
        #print '%s | %s (%s)' % (s1_tmp, s2_tmp, dist)

        if dist >= operation['threshold'] * c:
            return dist * 100.0
        if not restore:
            s1 = s1_tmp
            s2 = s2_tmp

    if dist > 0.75:
        return dist * 100

    l1 = num_words(s1)
    l2 = num_words(s2)
    if l1 == 0 or l2 == 0:
        return

    len_ratio = float(max(l1, l2)) / min(l1, l2)

    if l1 > 2 and l2 > 2 and len_ratio >= 1.5:
        if is_substring_of(s1, s2) or is_substring_of(s2, s1):
            return 75


def lower_strip(name):
    name = unicode(name.lower().strip())
    name_fixed = []
    for word in name.split():
        if word in AND_WORDS:
            name_fixed.append(u'&')
        else:
            name_fixed.append(word)
    return ' '.join(name_fixed).replace('\'', u'’').replace('\'', u'`')


def remove_punctuation2(name):
    return strip_punctuation(name).replace('(', '').replace(')', '').replace('/', '')


def remove_type(name):
    for beer_type in BEER_TYPES:
        if beer_type.lower() in name.lower():
            name = re.sub('(?i)' + re.escape(beer_type), '', name)
    return name.strip()

COMMON_WORDS = [
    u'Brewers Reserve',
    u'Bier',
    u'unfiltered',
]


def remove_common(name):
    for word in COMMON_WORDS:
        if word.lower() in name.lower():
            name = re.sub('(?i)' + re.escape(word), '', name)
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
        p = re.compile('\s\(.*?%s.*?\)') % packaging
        if p.search(name):
            name = name.replace(packaging, '')
    return name


def remove_size(name):
    return re.sub(r'(\d{1,4} cl)', '', name).strip()


def remove_abv(name):
    return re.sub(r'(\(\d+(\.\d{1,2})?\s*%\))', '', name).strip()


def remove_year(name):
    return re.sub(r'(\(\d{4}\s*-\s*(\d{4})?\))', '', name).strip()


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


def filter_packaging(beer_list):
    res = []
    for beer in beer_list:
        name = beer['name'].lower()
        wanted = True
        for package_type in UNWANTED_PACKAGE_TYPES:
            if package_type.lower() in name:
                wanted = False
                break
        if wanted:
            res.append(beer)
    return res


def filter_abv_above(beer_list, abv):

    p = re.compile('\((\d{1,2}\.\d{1,2})?\s*%\)')
    res = []
    for beer in beer_list:
        m = p.search(beer['name'])
        if m:
            if float(m.groups()[0]) > abv:
                res.append(beer)
        else:
            res.append(beer)
    return res


class BeerNameMatcher(object):

    def __init__(self, brewery_name, beer_list, abv_over=None):
        self.brewery_name = unicode(brewery_name)
        self.beer_list = self._prepare(beer_list)
        self.blist = filter_packaging(beer_list)
        if abv_over:
            self.blist = filter_abv_above(self.blist, abv_over)

    def match_name(self, name):

        max_ratio = 0
        hit = None
        for beer in self.blist:
            r = ratio(name, beer['name'], self.brewery_name)
            if r and r > max_ratio:
                max_ratio = r
                hit = beer
        # print max_ratio
        if hit and max_ratio >= 75.0:
            return hit

        '''
        org_name = name

        def remove_brewery_name(beer_name):
            brewery_name = self.brewery_name.lower()
            return beer_name.replace(brewery_name, '')

        def remove_brewery_name_parts(beer_name):
            brewery_name = self.brewery_name.lower()
            for part in brewery_name.split(' '):
                beer_name = beer_name.replace(part, ' ')
            return beer_name.strip()

        operations = [lower_strip, remove_brewery_name,
                      remove_brewery_name_parts, remove_packaging,
                      remove_size, remove_abv, remove_year,
                      remove_punctuation2, remove_common, remove_type]

        for operation in operations:
            match, name = self._check_match(name, operation)
            if match:
                return match

        match = self._check_split(remove_brewery_name_parts(lower_strip(org_name)))

        if match:
            return match
        return None
        '''

    def _check_match(self, name1, operation):
        print operation.__name__
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

        threshold = 90
        if operation.__name__ == 'lower_strip':
            threshold = 97

        if highest['dist'] > threshold:
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
        dist = ratio(unicode(name1), unicode(name2))

        # UWRatio(unicode(name1), unicode(name2))
        # dist = Levenshtein.ratio(unicode(name1), unicode(name2))
        print '%s | %s (%s)' % (name1, name2, dist)
        return {
            'beer': beer,
            'dist': dist
        }

    def _prepare(self, beer_list):
        return [Beer(beer) for beer in beer_list]
