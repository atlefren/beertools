Beertools
=========

A collection of pyhon scripts to work with beer and brewery data.


Setup
-----

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt


polparser.py
------------
A script to fetch beers from Vinmonopolet, returns a flat json-structure. 
Use either as command line:

    python polparser.py destination.json

Or in your script:

    from polparser import read
    beers = read()

ratebeerparser.py
------------
A script to fetch beers from Ratebeer, returns a flat json-structure. 
Use either as command line:

    python ratebeerparser.py destination.json

Or in your script:

    from ratebeerparser import read
    beers = read()

brewerynamematcher.py
---------------------
A tool to match brewery names, tuned to match vinmonopolet against ratebeer.

Usage:

    from brewerynamematcher import BreweryNameMatcher
    matcher = BreweryNameMatcher(breweries) # a list of dicts with at leadt a "name" attribute
    match = matcher.match_name('brewery name') # returns dict from list or None

breweryname_compare.py
----------------------
Test comparisons. Expects data/polet.json and data/ratebeer.json to exists. 
Writes results to data/nomatch.txt and data/match.txt


Tests
-----
Run tests with

    python -m unittest tests










