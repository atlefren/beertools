# -*- coding: utf-8 -*-

import HTMLParser

html_parser = HTMLParser.HTMLParser()


def string_parser(val):
    s = html_parser.unescape(val.strip())
    if s == '':
        return None
    return s


def int_parser(val):
    try:
        return int(val)
    except ValueError:
        return None


def float_parser(val):
    try:
        return float(val)
    except ValueError:
        return None


def float_pol_parser(val):
    return float_parser(val.replace(',', '.'))


def bool_parser(val):
    if val == '1':
        return True
    return False
