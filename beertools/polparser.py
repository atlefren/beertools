# -*- coding: utf-8 -*-
import requests
from util import get_line_parser, parsers

from pytz import timezone
import dateutil.parser

URL = 'http://www.vinmonopolet.no/api/produkter'


FIELDS = [
    {'name': 'Datotid', 'parser': parsers.string_parser},
    {'name': 'Varenummer', 'parser': parsers.int_parser},
    {'name': 'Varenavn', 'parser': parsers.string_parser},
    {'name': 'Volum', 'parser': parsers.float_pol_parser},
    {'name': 'Pris', 'parser': parsers.float_pol_parser},
    {'name': 'Literpris', 'parser': parsers.float_pol_parser},
    {'name': 'Varetype', 'parser': parsers.string_parser},
    {'name': 'Produktutvalg', 'parser': parsers.string_parser},
    {'name': 'Butikkategori', 'parser': parsers.string_parser},
    {'name': 'Fylde', 'parser': parsers.int_parser},
    {'name': 'Friskhet', 'parser': parsers.int_parser},
    {'name': 'Garvestoffer', 'parser': parsers.int_parser},
    {'name': 'Bitterhet', 'parser': parsers.int_parser},
    {'name': 'Sodme', 'parser': parsers.int_parser},
    {'name': 'Farge', 'parser': parsers.string_parser},
    {'name': 'Lukt', 'parser': parsers.string_parser},
    {'name': 'Smak', 'parser': parsers.string_parser},
    {'name': 'Passertil01', 'parser': parsers.string_parser},
    {'name': 'Passertil02', 'parser': parsers.string_parser},
    {'name': 'Passertil03', 'parser': parsers.string_parser},
    {'name': 'Land', 'parser': parsers.string_parser},
    {'name': 'Distrikt', 'parser': parsers.string_parser},
    {'name': 'Underdistrikt', 'parser': parsers.string_parser},
    {'name': 'Argang', 'parser': parsers.string_parser},
    {'name': 'Rastoff', 'parser': parsers.string_parser},
    {'name': 'Metode', 'parser': parsers.string_parser},
    {'name': 'Alkohol', 'parser': parsers.float_pol_parser},
    {'name': 'Sukker', 'parser': parsers.float_pol_parser},
    {'name': 'Syre', 'parser': parsers.float_pol_parser},
    {'name': 'Lagringsgrad', 'parser': parsers.string_parser},
    {'name': 'Produsent', 'parser': parsers.string_parser},
    {'name': 'Grossist', 'parser': parsers.string_parser},
    {'name': 'Distributor', 'parser': parsers.string_parser},
    {'name': 'Emballasjetype', 'parser': parsers.string_parser},
    {'name': 'Korktype', 'parser': parsers.string_parser},
    {'name': 'Vareurl', 'parser': parsers.string_parser},
]


def parse_line(line, parser):
    line = line.split(';')
    return parser(line)


def get_datetime(lines):
    # dt = all_products[0]['Datotid']
    dt = lines[1].split(';')[0]
    no_tz = timezone('Europe/Oslo')
    return no_tz.localize(
        dateutil.parser.parse(dt)
    )


def parse_lines(lines, parser):
    for line in lines[1:]:
        product = parse_line(line, parser)
        if product['Varetype'] == u'Øl':
            yield product


def read():
    r = requests.get(URL)
    r.encoding = 'ISO-8859-1'
    lines = r.text.splitlines()
    parser = get_line_parser(FIELDS)
    # all_products = [parse_line(line, parser) for line in lines[1:]]

    # beers = [product for product in all_products
    #         if product['Varetype'] == u'Øl']

    return parse_lines(lines, parser), get_datetime(lines)


if __name__ == '__main__':
    data, updated = read()
    print updated
    for d in data:
        print d
