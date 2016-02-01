# -*- coding: utf-8 -*-

from util import (get_zipfile, read_zipfile, parse_csv_file, parsers,
                  get_line_parser, get_datetime_for_zip)

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
        zipfile = read_zipfile(filename)
    else:
        zipfile = get_zipfile(URL)
    updated = get_datetime_for_zip(zipfile, 'brewers.csv')
    contents = zipfile.open('brewers.csv')
    return parse_csv_file(contents, get_line_parser(FIELDS)), updated

if __name__ == '__main__':
    data, updated = read()
    print updated
    for d in data:
        print d
