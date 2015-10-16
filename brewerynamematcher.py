# -*- coding: utf-8 -*-
import re


COMMON = [
    'Bryggeri',
    'brasserie de l’',
    'Brasserie de la '
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
        if equals:
            return True
    return False


def match_name(name, brewery_list):

    for brewery in brewery_list:
        if compare_breweries(name, brewery['name']):
            return brewery

    return None
