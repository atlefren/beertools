# -*- coding: utf-8 -*-
import sys
import json

import requests


URL = 'http://www.vinmonopolet.no/api/produkter'


FIELDS = [
    'Datotid', 'Varenummer', 'Varenavn', 'Volum', 'Pris', 'Literpris',
    'Varetype', 'Produktutvalg', 'Butikkategori', 'Fylde', 'Friskhet',
    'Garvestoffer', 'Bitterhet', 'Sodme', 'Farge', 'Lukt', 'Smak',
    'Passertil01', 'Passertil02', 'Passertil03', 'Land', 'Distrikt',
    'Underdistrikt', 'Argang', 'Rastoff', 'Metode', 'Alkohol', 'Sukker',
    'Syre', 'Lagringsgrad', 'Produsent', 'Distributør', 'Grossist',
    'Emballasjetype', 'Korktype', 'Vareurl'
]


def parse_line(line):
    fields = line.split(';')

    product = {}
    for index, name in enumerate(FIELDS):
        product[name] = fields[index]
    return product


def read():
    r = requests.get(URL)
    r.encoding = 'ISO-8859-1'
    lines = r.text.splitlines()
    all_products = [parse_line(line) for line in lines[1:]]
    return [product for product in all_products
            if product['Varetype'] == u'Øl']


if __name__ == '__main__':
    outfile = sys.argv[1]

    with open(outfile, 'w') as out:
        out.write(json.dumps(read(), indent=4))
