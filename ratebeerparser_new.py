# -*- coding: utf-8 -*-
import zipfile
import io
import sys
import json

import requests

from util.unicodereader import UnicodeReader
from util import parsers


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


def get_file_disk(filename):
    return zipfile.ZipFile(filename)


def get_file():
    r = requests.get(URL, stream=True)
    s = io.BytesIO()
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            s.write(chunk)
            s.flush()
    return zipfile.ZipFile(s)


def parse_line(line):
    obj = {}
    for value, key in zip(line, FIELDS):
        obj[key['name']] = key['parser'](value)
    return json.dumps(obj, indent=4)


def parse_file(contents):
    reader = UnicodeReader(contents)
    return [parse_line(line) for line in reader]


def read():
    contents = get_file_disk('data/beers_new.zip')
    # contents = get_file()
    return parse_file(contents.open('beers.csv'))


if __name__ == '__main__':
    outfile = sys.argv[1]
    with open(outfile, 'w') as out:
        out.write(json.dumps(read(), indent=4))
