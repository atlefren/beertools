# -*- coding: utf-8 -*-

from util import (get_zipfile, read_zipfile, parse_csv_file, parsers,
                  get_line_parser, get_datetime_for_zip)

URL = 'http://66.135.55.93/documents/downloads/beers.zip'

FIELDS = [
    {'name': 'id', 'parser': parsers.int_parser},
    {'name': 'name', 'parser': parsers.string_parser},
    {'name': 'brewery_id', 'parser': parsers.int_parser},
    {'name': 'shortname', 'parser': parsers.string_parser},
    {'name': 'abv', 'parser': parsers.float_parser},
    {'name': 'ibu', 'parser': parsers.float_parser},
    {'name': 'style_id', 'parser': parsers.int_parser},
    {'name': 'style', 'parser': parsers.string_parser},
    {'name': 'score_overall', 'parser': parsers.int_parser},
    {'name': 'score_style', 'parser': parsers.int_parser},
    {'name': 'alias', 'parser': parsers.bool_parser},
    {'name': 'retired', 'parser': parsers.bool_parser},
]


def read(filename=None):
    if filename is not None:
        zipfile = read_zipfile(filename)
    else:
        zipfile = get_zipfile(URL)
    updated = get_datetime_for_zip(zipfile, 'beers.csv')
    contents = zipfile.open('beers.csv')
    return parse_csv_file(contents, get_line_parser(FIELDS)), updated
