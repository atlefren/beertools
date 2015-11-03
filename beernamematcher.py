# -*- coding: utf-8 -*-

import re
import unicodedata

import Levenshtein

from brewerynamematcher import strip_punctuation

BEER_TYPES = [
    u'American Pale Ale',
    u'Abbey Brown Ale',
    u'Barleywine',
    u'Imperial Wheat Stout',
    u'Imperial Coffee Stout',
    u'Imperial Stout',
    u'Imperial Red Ale',
    u'Imperial Black IPA',
    u'Imperial Raspberry Stout',
    u'Imperial IPA',
    u'Imperial Pils',

    u'India Pale Ale',
    u'India Red Ale',
    u'Indian Pale Ale',
    u'India Dark Ale',

    u'Irish Stout',
    u'Oyster Stout',
    u'Milk Stout',

    u'Brown Ale',
    u'Belgian Ale',
    u'Pale Ale',
    u'Amber Ale',
    u'Blonde Ale',
    u'Blond Ale',

    u'White IPA',
    u'Saison IPA',
    u'Rye IPA',
    u'Session IPA',
    u'Dobbel IPA',
    u'Double IPA',
    u'Black IPA',
    u'Amber IPA',
    u'Red IPA',
    u'DIPA',
    u'IPA',
    u'APA',
    u'Farmhouse Ale',
    u'Dubbel Bruin',

    u'Ancient Grains Ale',

    u'Blonde',

    u'Geuze',

    u'Saison',

    u'Lager',
    u'Pils',

    u'Cream Stout',
    u'Stout Porter',
    u'Imperial Porter',
    u'London Porter',
    u'Porter',

    u'Dubbel Witbier',
    u'Dunkles Weizen',
    u'Witbier',
    u'Wit',

    u'Hefe Weizen',
    u'Hefeweizen',
    u'Berliner Weisse',
    u'Weizenbock',
    u'Weissbier',
    u'Winterbier',
    u'Wheat Beer',

    u'Belgian Tripel',
    u'Trippel',
    u'Triple',
    u'Tripel',

    u'Dubbel',
    u'Ambree',

    u'Rich Ale',
]

BEER_TYPES = [x.lower() for x in BEER_TYPES]

AND_WORDS = [
    u'og',
    u'and'
]

WANTED_PACKAGE_TYPES = [
    u' (bottle)',
    u' (bottle / keg)',
    u' (bottle / can)',
    u' (cask & bottle conditioned)',
    u' (pasteurized)',
    u' (pasteurised)',
    u' (filtered)',
]

UNWANTED_PACKAGE_TYPES = [
    u'cask',
    u'keg'
]

COMMON_WORDS2 = [
    u'Brewers Reserve',
    u'Brewery',
    u'Barrel-Aged',
    u'barrel aged',
    u'Single Hopped',
    u'originalen',
    u'unfiltered',
    u'brewing',
    u'Brasserie',
    u'project',
    u'Økologisk',
    u'Single Hop',
    u'Magnum Edition',
    u'Handgeplukte',
    u'Trappistenbier',
    u'Trappistes',
    u'Trappist',
    u'Craft',
    u'Premium',
    u'Mini Keg',
    u'Seasonal',
    u'Rye',
    u'Herb',
    u'Brettanomyces',
    u'edition',
    u'lys',
    u'Amerikansk',
    u'Bayersk',
    u'Belgisk',
    u'Extra',
    u'Danish',
    u'special reserve ale',
    u'year old',
    u'Single Batch',
    u'Original'
]

SYNONYMS = {
    'blonde': ['blond'],
    'red': ['rouge'],
    'unfiltered': ['non filtrata'],
    'lager': ['lager / pilsner', u'lageröl'],
    'extra': ['ekstra'],
    'brown': ['brune', 'bruin'],
    'dunkel': ['dark'],
    'pils': ['pilsner', 'pilsener', 'pilsen'],
    'ipa': ['india pale ale'],
    'noire': ['noir'],
    'bio': ['biologique'],
    'oude': ['oudbeitje'],
    'kriek': ['krieken'],
    'lambic': ['lambik'],
    'rye': ['rug'],
    'trippel': ['triple', 'tripel'],
}


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


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
    return remove_accents(' '.join(s.split()))


def fix_typography(name):
    name = name.replace(u'’', '\'').replace('`', u'\'').replace('\'s', u's')
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
    words = [remove_accents(w) for w in words]
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


def remove_synonyms(name):
    name = remove_accents(unicode(name))
    name = ' %s ' % name
    for word, duplicates in SYNONYMS.iteritems():
        for duplicate in duplicates:
            duplicate = remove_accents(unicode(duplicate))
            regex = '(?<![a-z])(%s)(?![a-z])' % duplicate
            p = re.compile(regex)
            name = p.sub(word, name)
    return name.strip()


def remove_duplicates(name):
    name = name.split()
    return ' '.join(unique_list(name, SYNONYMS.keys()))


def shift_range(value):
    return (((value - 0.0) * (100.0 - 90.0)) / (100.0 - 0.0)) + 90.0


def remove_collab(name):
    if '/' in name and name.index('/') < len(name) / 2.0:
        name_last = name[name.index('/') + 1:].strip()
        name = ' '.join(name_last.split()[1:])
    return name


def remove_in_parentesis(name):
    p = re.compile(r'(\(.*?\))')
    return p.sub('', name).strip()


def is_substring_of(s1, s2):
    return s1 in s2


def num_words(s):
    return len(s.split())


def sort_words(s):
    return ' '.join(sorted(s.split()))


def remove_after_semicolon(s):
    if ':' in s:
        return s[0:s.index(':')]
    return s


def sort_and_join(name):
    return ''.join(sort_words(name).split(' '))


def ratio(s1, s2, brewery_name):
    s1 = unicode(s1)
    s2 = unicode(s2)
    org1 = s1
    org2 = s2
    brewery_name = remove_accents(brewery_name.lower())

    def remove_brewery(name):
        res = remove_from_str(name, brewery_name)
        if res == name:
            res = remove_from_str(name, brewery_name.replace(' ', ''))
        return res

    def remove_brewery_parts(name):
        return remove_from_str_parts(name, brewery_name)

    operations = [
        {'func': lower_strip2, 'threshold': 0.93},
        {'func': fix_typography, 'threshold': 0.93},
        {'func': sort_and_join, 'threshold': 0.93, 'restore': True},
        {'func': remove_collab, 'threshold': 0.93},
        {'func': remove_brewery, 'threshold': 0.93},
        {'func': remove_brewery_parts, 'threshold': 0.93},
        {'func': remove_packaging2, 'threshold': 0.93},
        {'func': fix_and_words, 'threshold': 0.93},
        {'func': remove_synonyms, 'threshold': 0.93},
        {'func': remove_abv2, 'threshold': 0.93},
        {'func': remove_year2, 'threshold': 0.93},
        {'func': remove_size2, 'threshold': 0.93},
        {'func': remove_in_parentesis, 'threshold': 0.85, 'restore': True},
        {'func': remove_after_semicolon, 'threshold': 0.93, 'restore': True},
        {'func': remove_punctuation3, 'threshold': 0.93},
        {'func': sort_words, 'threshold': 0.93, 'restore': True},
        {'func': remove_common2, 'threshold': 0.93, 'restore': True},
        {'func': remove_type2, 'threshold': 0.93, 'restore': True},
        {'func': remove_duplicates, 'threshold': 0.90},
        {'func': remove_common2, 'threshold': 0.90},
        {'func': remove_type2, 'threshold': 0.8},
        {'func': remove_single_year, 'threshold': 0.90},
        {'func': sort_words, 'threshold': 0.90, 'restore': True},
    ]
    length = len(operations)
    index = 0

    #print '--'
    for operation in operations:
        restore = operation.get('restore', False)

        s1_tmp = operation['func'](s1)
        s2_tmp = operation['func'](s2)

        if s1_tmp == '' or s1_tmp == '':
            restore = True

        if s1 == s1_tmp and s2 == s2_tmp:
            c = 1
        else:
            c = shift_range(float(length - index) / float(length) * float(100)) / 100.0
        dist = Levenshtein.ratio(unicode(s1_tmp), unicode(s2_tmp)) * c

        if s1_tmp == '' and s2_tmp == '':
            dist = 0.0

        threshold = operation['threshold'] * c
        #print operation['func'].__name__
        #print '%s | %s (%s) (%s)' % (s1_tmp, s2_tmp, dist, threshold)
        if dist >= threshold:
            ratio = 100.0
            if operation['func'].__name__ != 'sort_and_join':
                if num_words(s1_tmp) < 2 or num_words(s2_tmp) < 2:
                    ratio = shift_range(Levenshtein.ratio(unicode(org1), unicode(org2)))
            return dist * ratio
        if not restore:
            s1 = s1_tmp
            s2 = s2_tmp
        if not restore:
            index = index + 1

    l1 = num_words(s1)
    l2 = num_words(s2)
    if l1 == 0 or l2 == 0:
        return

    len_ratio = float(max(l1, l2)) / min(l1, l2)

    if l1 >= num_words(org1) / 2 and l2 >= num_words(org2) / 2 and len_ratio >= 1.5:
        if is_substring_of(s1, s2) or is_substring_of(s2, s1):
            return 75


def filter_packaging(beer_list):
    res = []
    for beer in beer_list:
        name = fix_typography(beer['name'].lower())
        wanted = True
        for package_type in UNWANTED_PACKAGE_TYPES:
            if package_type.lower() in name:
                wanted = False
                for wanted_type in WANTED_PACKAGE_TYPES:
                    if wanted_type.lower() in name:
                        wanted = True
                        break
        if wanted:
            res.append(beer)
    return res


def abv_by_regex(name):
    p = re.compile('\((\d{1,2}\.\d{1,2})?\s*%\)')
    m = p.search(name)
    if m:
        return float(m.groups()[0])
    return None


def filter_abv_above(beer_list, abv_limit):
    res = []
    for beer in beer_list:
        if 'abv' in beer:
            abv = beer['abv']
        else:
            abv = abv_by_regex(beer['name'])
        if abv:
            if abv > abv_limit:
                res.append(beer)
        else:
            res.append(beer)
    return res


def skip_retired_beers(beer_list):
    return [beer for beer in beer_list if not beer.get('retired', False)]


class BeerNameMatcher(object):

    def __init__(self, brewery_name, beer_list, abv_over=None, skip_retired=False):
        self.brewery_name = unicode(brewery_name)
        self.blist = filter_packaging(beer_list)
        self.skip_retired = skip_retired
        self.abv_over = abv_over

    def match_name(self, name, skip_retired=None, use_abv_over=True):

        beer_list = self.blist

        if skip_retired is None:
            skip_retired = self.skip_retired

        if use_abv_over and self.abv_over is not None:
            beer_list = filter_abv_above(beer_list, self.abv_over)

        if skip_retired:
            beer_list = skip_retired_beers(beer_list)

        max_ratio = 0
        hit = None
        for beer in beer_list:
            r = ratio(name, beer['name'], self.brewery_name)
            if r and r >= max_ratio:
                if r == max_ratio:
                    prev_ratio = Levenshtein.ratio(unicode(name), unicode(hit['name']))
                    new_ratio = Levenshtein.ratio(unicode(name), unicode(beer['name']))
                    if new_ratio > prev_ratio:
                        hit = beer
                else:
                    max_ratio = r
                    hit = beer
        if hit and max_ratio >= 75.0:
            return hit

        if skip_retired:
            return self.match_name(name, skip_retired=False)

        if use_abv_over and self.abv_over is not None:
            return self.match_name(name, skip_retired=False, use_abv_over=False)
