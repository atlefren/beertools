# -*- coding: utf-8 -*-

from util import read_json


rb_countries = read_json('geoloc/ratebeer_countries.json')
iso_countries = read_json('geoloc/3166-1alpha-2.json')

breweries = read_json('data/rb_breweries.json')


for brewery in breweries:

    print rb_countries[str(brewery['country'])]

