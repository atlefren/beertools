# -*- coding: utf-8 -*-
import sys
import json

from util import (get_zipfile, read_zipfile, parse_csv_file, parsers,
                  get_line_parser)

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
        contents = read_zipfile(filename, 'beers.csv')
    else:
        contents = get_zipfile(filename, 'beers.csv')
    return parse_csv_file(contents, get_line_parser(FIELDS))


if __name__ == '__main__':
    outfile = sys.argv[1]
    filename = None
    if len(sys.argv) > 2:
        filename = sys.argv[2]
    with open(outfile, 'w') as out:
        out.write(json.dumps(read(filename), indent=4))
