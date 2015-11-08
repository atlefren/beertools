# -*- coding: utf-8 -*-
import sys
import json
from beertools import read_ratebeer_breweries

if __name__ == '__main__':
    outfile = sys.argv[1]
    filename = None
    if len(sys.argv) > 2:
        filename = sys.argv[2]
    with open(outfile, 'w') as out:
        out.write(json.dumps(read_ratebeer_breweries(filename), indent=4))
