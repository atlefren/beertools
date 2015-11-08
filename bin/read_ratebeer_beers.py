# -*- coding: utf-8 -*-
import sys
import json
import os

from beertools import read_ratebeer_beers

if __name__ == '__main__':
    outfile = sys.argv[1]
    filename = None
    if len(sys.argv) > 2:
        filename = sys.argv[2]

    path = os.path.join(os.getcwd(), outfile)
    with open(path, 'w') as out:
        out.write(json.dumps(read_ratebeer_beers(filename), indent=4))
