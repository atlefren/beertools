# -*- coding: utf-8 -*-
import re


COMMON = [
    u'Bierbrouwerij',
    u'Bryggeri & Spiseri',
    u'Mikrobryggeri',
    u'Microbirrificio',
    u'Bryggerhuset',
    u'Bryggerier',
    u'Bryggeriet',
    u'Bryggeri',
    u'brasserie de l’',
    u'Brasserie de la ',
    u'Brewery',
    u'Brewing Company',
    u'Brewing Co.',
    u'Brewing Co',
    u'Brewing',
    u'Picobrouwerij',
    u'Microbrouwerij',
    u'Brouw.',
    u'Brouwerij',
    u'Brygghus',
    u'Bryghus',
    u'Birra',
    u'Brasserie',
    u'Craft Beer',
    u'Beer',
    u'Bieres',
    u' SA',
    u'Le ',
    u'De ',
    u' AS',
]


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


def compare(name1, name2, operator):
    name1 = operator(name1)
    name2 = operator(name2)
    return name1, name2, name1 == name2


def compare_breweries(name1, name2):

    operators = [clean, remove_corporation, remove_common]

    for operator in operators:
        name1, name2, equals = compare(name1, name2, operator)
#        print name1, name2
        if equals:
            return True
    return False


def match_name(name, brewery_list):

    for brewery in brewery_list:
        if compare_breweries(name, brewery['name']):
            return brewery

    return None
