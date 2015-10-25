# -*- coding: utf-8 -*-
import sys
from util import read_json


if __name__ == '__main__':
    beers = read_json('data/rb_beers.json')
    brewery_id = int(sys.argv[1])

    for beer in [item for item in beers if item['brewery_id'] == brewery_id]:
        print beer['name']
