# -*- coding: utf-8 -*-
import zipfile
import requests
import io
import json

from unicodereader import UnicodeReader


def get_zipfile(url, filename):
    r = requests.get(url, stream=True)
    s = io.BytesIO()
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            s.write(chunk)
            s.flush()
    return zipfile.ZipFile(s).open(filename)


def read_zipfile(zipfilename, filename):
    return zipfile.ZipFile(zipfilename).open(filename)


def parse_csv_file(contents, parse_line):
    reader = UnicodeReader(contents)
    return [parse_line(line) for line in reader]


def get_line_parser(fields):
    def parse_line(line):
        obj = {}
        for value, key in zip(line, fields):
            obj[key['name']] = key['parser'](value)
        return obj
    return parse_line


def read_json(filename):
    with open(filename, 'r') as infile:
        return json.loads(infile.read())
