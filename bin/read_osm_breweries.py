# -*- coding: utf-8 -*-
import sys
import json
import os

from beertools import get_osm_breweries


if __name__ == '__main__':
    country = sys.argv[1]
    outfile = sys.argv[2]

    path = os.path.join(os.getcwd(), outfile)
    with open(path, 'w') as out:
        breweries = get_osm_breweries(country)
        out.write(json.dumps(breweries, indent=4))
