# -*- coding: utf-8 -*-
import sys
import json
from beertools import read_ratebeer_breweries
import os


if __name__ == '__main__':
    outfile = sys.argv[1]
    filename = None
    if len(sys.argv) > 2:
        filename = sys.argv[2]

    path = os.path.join(os.getcwd(), outfile)
    with open(path, 'w') as out:
        breweries, updated = read_ratebeer_breweries(filename)
        out.write(json.dumps(breweries, indent=4))
