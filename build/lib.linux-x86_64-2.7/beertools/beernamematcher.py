# -*- coding: utf-8 -*-

import re
from unidecode import unidecode

import Levenshtein

from brewerynamematcher import strip_punctuation

BEER_TYPES = [
    u'American Pale Ale',
    u'Abbey Brown Ale',
    u'Barleywine',
    u'Imperial Wheat Stout',
    u'Imperial Coffee Stout',
    u'Imperial Stout',
    u'Imperial Porter ale',
    u'Imperial Porter',
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
    u'Blonde',

    u'Golden ale',

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

    u'Amber',
    u'Geuze',

    u'Saison',

    u'Bockbier',

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
    u'Wit Bier',
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
    u'bottle / keg',
    u'bottle / can',
    u'cask & bottle conditioned',
    u'pasteurized',
    u'pasteurised',
    u'filtered',
    u'bottle',
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
    u'belgian',
    u'Extra',
    u'Danish',
    u'special reserve ale',
    u'year old',
    u'Single Batch',
    u'Original',
    u'Famous',
    u'Batch',
    u'hell',
    u'chapeau',
    u'bottle refermented',
    u'Birra',
    u'Real',
    u'Superior Hoppig',
    u'Artisanale',
    u'classic'
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
    'nr': ['Nr.', 'No'],
    'blonde': ['blond ale', 'blonde ale', 'blond']
}


def remove_accents(input_str):
    return unidecode(input_str)


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


def lower_strip(s):
    s = s.lower().strip()
    return remove_accents(' '.join(s.split()))


def fix_typography(name):
    name = name.replace(u'’', '\'').replace('`', u'\'').replace('\'s', u's')
    p = re.compile('([a-z])/([a-z])')
    return p.sub(r'\1 / \2', name)


def remove_packaging(name):
    for packaging in WANTED_PACKAGE_TYPES:
        p = re.compile('\((.*?)%s(.*?)\)' % packaging)
        name = p.sub(r'(\1\2)', name)
        name = name.replace('()', '').strip()
    return name


def remove_size(name):
    return re.sub(r'(\d{1,4} cl)', '', name).strip()


def remove_abv(name):
    name = re.sub(r'(\(\d+(\.\d{1,2})?\s*%\))', '', name).strip()
    return re.sub(r'(\d{1,2}\.?\d{0,4}\s*%)', '', name).strip()


def remove_year(name):
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


def remove_type(name):
    return remove_words(name, BEER_TYPES)


def remove_common(name):
    return remove_words(name, COMMON_WORDS2)


def remove_punctuation(name):
    return strip_punctuation(name) \
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


def remove_all_duplicates(name):
    name = name.split()
    return ' '.join(unique_list(name, name))


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


def skip_retired_beers(beer_list):
    return [beer for beer in beer_list if not beer.get('retired', False)]


def is_within_range(n1, n2, diff):
    return abs(n1 - n2) <= diff


def punishment_by_list(length, index):
    shifted = shift_range(float(length - index) / float(length) * float(100))
    return shifted / 100.0


class BeerNameMatcher(object):

    def __init__(self, brewery_name, beer_list, skip_retired=False):
        brewery_name = unicode(brewery_name)
        self.brewery_name = remove_accents(brewery_name.lower())

        beer_list = filter_packaging(beer_list)
        self.skip_retired = skip_retired
        self.stats_list = self.generate_stats_list(beer_list)

    def generate_stats_list(self, beer_list):
        stats = []
        for beer in beer_list:
            stats.append({
                'beer': beer,
                'stats': self.generate_stats(beer['name'], self.brewery_name)
            })
        return stats

    def match_name(self, name, skip_retired=None, abv=None):

        if skip_retired is None:
            skip_retired = self.skip_retired

        b1 = self.generate_stats(name, self.brewery_name)

        max_ratio = 0
        hit = None
        for stat in self.stats_list:
            beer = stat['beer']
            beer_abv = beer.get('abv', None)
            if abv and beer_abv:
                abv_match = is_within_range(abv, beer_abv, 0.5)
                if not abv_match:
                    continue

            beer_retired = beer.get('retired', False)
            if skip_retired and beer_retired:
                continue

            r = self.ratio2(b1, stat['stats'])
            if r:
                r = round(r, 1)
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

    def generate_stats(self, beername, brewery_name):

        operations = self.get_operations()

        beername = unicode(beername)

        res = {}
        res['org_name'] = beername
        s1 = beername
        for operation in operations:
            restore = operation.get('restore', False)
            s1_tmp = operation['func'](s1)
            if s1_tmp == '' or s1_tmp == '':
                restore = True
            res[operation['name']] = s1_tmp
            if not restore:
                s1 = s1_tmp
        return res

    def ratio2(self, b1, b2):
        operations = self.get_operations()

        s1 = b1['org_name']
        s2 = b2['org_name']
        org1 = s1
        org2 = s2

        length = len(operations)

        index = 0
        max_score = 0

        for operation in operations:

            # Shold this operation be restored?
            restore = operation.get('restore', False)

            # Perform operation
            s1_tmp = b1[operation['name']]
            s2_tmp = b2[operation['name']]

            # if one of the resulting strings is empty, restore operation
            if s1_tmp == '' or s1_tmp == '':
                restore = True

            # if the operation does not change strings, no "punishment"
            if s1 == s1_tmp and s2 == s2_tmp:
                c = 1
            else:
                # the punishment gets larger the further down in the
                # operations list we get
                c = punishment_by_list(length, index)

            # calculate distance (with puhishment)
            dist = Levenshtein.ratio(unicode(s1_tmp), unicode(s2_tmp)) * c

            # distance is zero if both strings empty
            if s1_tmp == '' and s2_tmp == '':
                dist = 0.0

            # adjust threshold to index
            threshold = operation['threshold'] * c

            # print operation['name']
            # print '%s | %s (%s) (%s)' % (s1_tmp, s2_tmp, dist, threshold)

            # if above threshold, things gets interesting!
            if dist >= threshold:
                ratio = 100.0
                if operation['name'] != 'sort_and_join':
                    if num_words(s1_tmp) < 2 or num_words(s2_tmp) < 2:

                        # adjust ratio by original difference
                        ratio = shift_range(Levenshtein.ratio(unicode(org1), unicode(org2)))
                # tune the distance
                score = dist * ratio

                # store maximum score
                if score > max_score:
                    max_score = score

            # use the values calculated here in next step (if not restore)
            if not restore:
                s1 = s1_tmp
                s2 = s2_tmp

            # make sure pushishment isn't increased if we restore
            if not restore:
                index = index + 1

        # if score above threshold, return it
        if max_score > 60:
            return max_score

        # check if there still are stuff to compare on
        l1 = num_words(s1)
        l2 = num_words(s2)
        if l1 == 0 or l2 == 0:
            return

        # substring check
        len_ratio = float(max(l1, l2)) / min(l1, l2)
        if l1 >= num_words(org1) / 2 and l2 >= num_words(org2) / 2 and len_ratio >= 1.5:
            if is_substring_of(s1, s2) or is_substring_of(s2, s1):
                return 75

    def remove_brewery(self, name):
        res = remove_from_str(name, self.brewery_name)
        if res == name:
            res = remove_from_str(name, self.brewery_name.replace(' ', ''))
        return res

    def remove_brewery_parts(self, name):
        return remove_from_str_parts(name, self.brewery_name)

    def get_operations(self):
        return [
            {'name': 'lower_strip', 'func': lower_strip, 'threshold': 0.93},
            {'name': 'fix_typography', 'func': fix_typography, 'threshold': 0.93},
            {'name': 'sort_and_join', 'func': sort_and_join, 'threshold': 0.93, 'restore': True},
            {'name': 'remove_collab', 'func': remove_collab, 'threshold': 0.93},
            {'name': 'remove_brewery', 'func': self.remove_brewery, 'threshold': 0.93},
            {'name': 'remove_brewery_parts', 'func': self.remove_brewery_parts, 'threshold': 0.93},
            {'name': 'remove_packaging', 'func': remove_packaging, 'threshold': 0.93},
            {'name': 'fix_and_words', 'func': fix_and_words, 'threshold': 0.93},
            {'name': 'remove_synonyms', 'func': remove_synonyms, 'threshold': 0.93},
            {'name': 'remove_abv', 'func': remove_abv, 'threshold': 0.93},
            {'name': 'remove_year', 'func': remove_year, 'threshold': 0.93},
            {'name': 'remove_size', 'func': remove_size, 'threshold': 0.93},
            {'name': 'remove_in_parentesis', 'func': remove_in_parentesis, 'threshold': 0.85, 'restore': True},
            {'name': 'remove_after_semicolon', 'func': remove_after_semicolon, 'threshold': 0.93, 'restore': True},
            {'name': 'remove_punctuation', 'func': remove_punctuation, 'threshold': 0.93},
            {'name': 'sort_words', 'func': sort_words, 'threshold': 0.93, 'restore': True},
            {'name': 'remove_common', 'func': remove_common, 'threshold': 0.93, 'restore': True},
            {'name': 'remove_type', 'func': remove_type, 'threshold': 0.93, 'restore': True},
            {'name': 'remove_duplicates', 'func': remove_duplicates, 'threshold': 0.90},
            {'name': 'remove_common2', 'func': remove_common, 'threshold': 0.90},
            {'name': 'remove_type2', 'func': remove_type, 'threshold': 0.8},
            {'name': 'remove_single_year', 'func': remove_single_year, 'threshold': 0.90},
            {'name': 'sort_words2', 'func': sort_words, 'threshold': 0.90, 'restore': True},
            {'name': 'remove_all_duplicates', 'func': remove_all_duplicates, 'threshold': 0.90, 'restore': True},
        ]
