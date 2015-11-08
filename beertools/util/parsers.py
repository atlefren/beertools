# -*- coding: utf-8 -*-

import HTMLParser

html_parser = HTMLParser.HTMLParser()


def string_parser(val):
    return html_parser.unescape(val.strip())


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


def bool_parser(val):
    if val == '1':
        return True
    return False
