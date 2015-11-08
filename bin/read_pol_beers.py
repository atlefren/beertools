# -*- coding: utf-8 -*-
import sys
import json
import os

from beertools import read_pol_beers


if __name__ == '__main__':
    outfile = sys.argv[1]

    path = os.path.join(os.getcwd(), outfile)
    with open(path, 'w') as out:
        out.write(json.dumps(read_pol_beers(), indent=4))
