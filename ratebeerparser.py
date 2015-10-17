# -*- coding: utf-8 -*-

import zipfile
import io
import HTMLParser
import sys
import json

import requests


URL = 'http://www.ratebeer.com/documents/downloads/beers.zip'
FIELDS = ['id', 'name', 'short_name', 'brewery', 'num1', 'num2']


def parse_line(line):
    html_parser = HTMLParser.HTMLParser()
    fields = [html_parser.unescape(col.strip())
              for col in line.split('\t') if col.strip() != '']

    diff = len(FIELDS) - len(fields)
    if diff > 0:
        fields.extend(['' for i in range(diff)])

    product = {}
    for index, name in enumerate(FIELDS):
        product[name] = fields[index]
    return product


def get_file():
    r = requests.get(URL, stream=True)
    s = io.BytesIO()
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            s.write(chunk)
            s.flush()
    zp = zipfile.ZipFile(s)
    return zp.read('beers.txt').decode('UTF-16')


def get_file_disk(filename):
    zp = zipfile.ZipFile(filename)
    return zp.read('beers.txt').decode('UTF-16')


def read():
    # lines = get_file_disk('data/beers.zip')
    lines = get_file()
    return [parse_line(line) for line in lines.splitlines()]


if __name__ == '__main__':
    outfile = sys.argv[1]
    with open(outfile, 'w') as out:
        out.write(json.dumps(read(), indent=4))
