# -*- coding: utf-8 -*-
import re
import Levenshtein
import string

COMMON = [
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
    for common in COMMON:
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


known_misspellings = [
    {'name': u'Bayerische Staatsbrauerei Weihenstephan', 'misspellings': [u'Weihenstephan Bayerische Staat']},
    {'name': u'Boon Rawd Brewery', 'misspellings': [u'Singha Corporation Co. Ltd.']},
    {'name': u'Brauerei Landsberg', 'misspellings': [u'Braukunst Berlin']},
    {'name': u'Brauerei Gusswerk', 'misspellings': [u'Meinklang']},
    {'name': u'Brasserie Rochefort', 'misspellings': [u'Abbaye St-Remy']},
    {'name': u'Brouwerij der Trappistenabdij De Achelse Kluis', 'misspellings': [u'Achel Brewery']},
    {'name': u'Brouwerij F. Boon', 'misspellings': [u'Brouw. Boon']},
    {'name': u'Brouwerij Malheur (formerly De Landtsheer)', 'misspellings': [u'Brouwerij de Landtsheer']},
    {'name': u'Brouwerij Omer Vander Ghinste', 'misspellings': [u'Browerij Bockor']},
    {'name': u'Cerveceria Birrart', 'misspellings': [u'Priorat Beer & Co']},
    # {'name': u'Charles Wells', 'misspellings': [u'Young & Co Brewery']},
    {'name': u'Coisbo Beer', 'misspellings': [u'Undercover Brewing']},
    {'name': u'Clan!Destino?', 'misspellings': [u'Carussin']},
    {'name': u'Cervecera Ceriux', 'misspellings': [u'Cervacera Artesana Fundada en']},
    # {'name': u'CRAK Brewery', 'misspellings': [u'CR/AK Brewery s.r.l.']},
    {'name': u'Damm', 'misspellings': [u'Estrella Damm']},
    {'name': u'De Proefbrouwerij', 'misspellings': [u'Gageleer']},
    {'name': u'Donkey Santorini Brewing Company', 'misspellings': [u'Santorini Brewing Company']},
    {'name': u'Duvel Moortgat', 'misspellings': [u'Moortgat']},
    {'name': u'Fuller’s', 'misspellings': [u'Fuller, Smith & Turner']},
    {'name': u'Green’s', 'misspellings': [u'Charles Cooper Ltd. Greens']},
    {'name': u'Greene King', 'misspellings': [u'Morland']},
    {'name': u'Hansa Borg Bryggerier', 'misspellings': [u'Borg Bryggerier']},
    {'name': u'Indslev Bryggeri', 'misspellings': [u'Ugly Duck Brewing Co.']},
    {'name': u'Klosterbrauerei Ettal', 'misspellings': [u'Benediktiner Weissbräu GmbH']},
    {'name': u'Královský pivovar Krušovice (Heineken)', 'misspellings': [u'Heineken Ceska Republika']},
    {'name': u'L’Esperluette', 'misspellings': [u'Robert Christoph']},
    {'name': u'Malmgårdin Panimo - Malmgard Brewery', 'misspellings': [u'Malmgården Panimo Oy', u'Malmgårds Bryggeri AB']},
    {'name': u'Nøgne Ø', 'misspellings': [u'Nøgne Ø Det kompromissløse Bry']},
    {'name': u'Pivovar Náchod (LIF)', 'misspellings': [u'Primator']},
    {'name': u'Schloßbrauerei Kaltenberg (Warsteiner)', 'misspellings': [u'König Ludwig']},
    {'name': u'Spendrups Bryggeri', 'misspellings': [u'Brutal Brewing']},
    {'name': u'Staatliches Hofbräuhaus München', 'misspellings': [u'Hofbräu']},
    {'name': u'Theresianer Antica Birreria di Trieste', 'misspellings': [u'Theresianer']},
    {'name': u'Thwaites', 'misspellings': [u'Crafty Dan Micro Brewery/Thwai', u'Craft Dan Micro Brewery/Thwait']},
    {'name': u'Tucher Bräu Fürth (Oetker Group)', 'misspellings': [u'Lederer']},
    {'name': u'United Breweries Group', 'misspellings': [u'United Breweries Group of Bang']},
    {'name': u'Vliegende Paard Brouwers', 'misspellings': [u'Prearis']},
    {'name': u'Wellpark (C&C Group)', 'misspellings': [u'Tennent Caledonian']},
]


class BreweryNameMatcher(object):

    def __init__(self, brewery_list):

        self.brewery_list = self._prepare(brewery_list)

    def _normalize(self, name):
        name = self._fix_misspelling(name)
        return remove_corporation(remove_collab(remove_stopwords(clean(name))))

    def _prepare(self, brewery_list):
        result = []
        for brewery in brewery_list:
            obj = {
                'brewery': brewery,
                'normalized': self._normalize(brewery['name'])
            }
            result.append(obj)
        return result

    def compare(self, name, name2, operator):
        name = operator(name)
        return name, name == name2

    def _fix_misspelling(self, name):
        for misspelling in known_misspellings:
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

    def _count_matches(self, name):
        name = strip_punctuation(name).split(' ')
        max_count = 0
        brewery = None
        for brewery_obj in self.brewery_list:
            count = 0
            for word in name:
                for word2 in strip_punctuation(brewery_obj['normalized']).split(' '):
                    if word not in [u'gmbh', u'group', u'united'] and len(word) > 3 and word == word2:
                        count = count + 1
            if count > 0 and count > max_count:
                max_count = count
                brewery = brewery_obj
        if brewery is not None:
            return brewery['brewery']
        return None

    def match_name(self, name):
        name = unicode(name)

        name = self._normalize(name)

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
