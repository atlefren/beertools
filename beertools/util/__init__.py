# -*- coding: utf-8 -*-
import zipfile
import requests
import io
import json
from datetime import datetime
from pytz import timezone

from unicodereader import UnicodeReader


def get_zipfile(url):
    r = requests.get(url, stream=True)
    s = io.BytesIO()
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            s.write(chunk)
            s.flush()
    return zipfile.ZipFile(s)


def read_zipfile(zipfilename):
    return zipfile.ZipFile(zipfilename)


def get_datetime_for_zip(zipfile, filename):
    info = zipfile.getinfo(filename)
    dt = info.date_time
    central_tz = timezone('US/Central')
    return central_tz.localize(
        datetime(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
    )


def parse_csv_file(contents, parse_line):
    reader = UnicodeReader(contents)
    for line in reader:
        yield parse_line(line)


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


def parse_pol_abv(s):
    return float(s.replace(',', '.'))
