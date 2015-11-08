Beertools
=========

A collection of pyhon scripts to work with beer and brewery data.


Setup
-----

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt


Install package
---------------

    pip install beertools


read_pol_beers
------------

A script to fetch beers from Vinmonopolet, returns a flat json-structure.
Use either as command line:

    python -m read_pol_beers destination.json

Or in your script:

    from beertools import read_pol_beers
    beers = read_pol_beers()


read_ratebeer_beers
-------------------

A script to fetch beers from Ratebeer, returns a flat json-structure. 

This script uses the new Ratebeer-dump, and includes more data, but not brewery 
names. Use ratebeer_breweries_parser.py and match on brewery_id

Use either as command line:

    python -m read_ratebeer_beers destination.json

Or in your script:

    from beertools import read_ratebeer_beers
    beers = read_ratebeer_beers()


read_ratebeer_breweries
-----------------------

Use either as command line:

    python -m read_ratebeer_breweries destination.json

Or in your script:

    from beertools import read_ratebeer_breweries
    breweries = read_ratebeer_breweries()


BreweryNameMatcher
---------------------
A tool to match brewery names, tuned to match vinmonopolet against ratebeer.

Usage:

    from beertools import BreweryNameMatcher
    matcher = BreweryNameMatcher(breweries) # a list of dicts with at least a "name" attribute
    match = matcher.match_name('brewery name') # returns dict from list or None


BeerNameMatcher
---------------------
A tool to match brewery names, tuned to match vinmonopolet against ratebeer.

Usage:

    from beertools import BeerNameMatcher
    matcher = BeerNameMatcher('brewery_name', beeer_list, skip_retired=True)
    match = matcher.match_name('beer_name', abv=4.5) # returns dict from list or None


Tests
-----
Run tests with

    cd beertools
    python -m unittest tests
