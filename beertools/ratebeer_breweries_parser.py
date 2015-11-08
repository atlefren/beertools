# -*- coding: utf-8 -*-

from util import (get_zipfile, read_zipfile, parse_csv_file, parsers,
                  get_line_parser)

URL = 'http://66.135.55.93/documents/downloads/brewers.zip'

FIELDS = [
    {'name': 'id', 'parser': parsers.int_parser},
    {'name': 'name', 'parser': parsers.string_parser},
    {'name': 'city', 'parser': parsers.string_parser},
    {'name': 'subregion', 'parser': parsers.int_parser},
    {'name': 'country', 'parser': parsers.int_parser},
]


def read(filename=None):
    if filename is not None:
        content = read_zipfile(filename, 'brewers.csv')
    else:
        content = get_zipfile(URL, 'brewers.csv')
    return parse_csv_file(content, get_line_parser(FIELDS))
