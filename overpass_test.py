# -*- coding: utf-8 -*-

import json

import overpass

from beertools import BreweryNameMatcher


def read_json(filename):
    with open(filename, 'r') as infile:
        return json.loads(infile.read())


def parse_bbox(bbox):
    components = [float(n) for n in bbox.split(',')]
    west = components[0]
    south = components[1]
    east = components[2]
    north = components[3]
    return (south, west, north, east)


def get_query(tags, south=None, west=None, north=None, east=None):

    bbox = None
    if south is not None and west is not None and north is not None and east is not None:
        bbox = '{south},{west},{north},{east}'.format(
            west=west,
            south=south,
            east=east,
            north=north
        )

    query = []
    for key, value in tags.iteritems():
        line = 'node[%s=%s]' % (key, value)
        if bbox:
            line += '(%s)' % bbox
        query.append(line)
    return '(%s)' % ';'.join(query)


def parse_brewery(feature):
    old_properties = feature.get('properties', {})
    properties = {
        'id': feature.get('id', None),
        'id': feature.get('id', None),
        'name': old_properties.get('name', None),
        'housenumber': old_properties.get('addr:housenumber', None),
        'city': old_properties.get('addr:city', None),
        'postcode': old_properties.get('addr:postcode', None),
        'street': old_properties.get('addr:street', None),
    }

    feature['properties'] = properties
    return feature


def get_osm_breweries(bbox):
    south, west, north, east = parse_bbox(bbox)

    api = overpass.API(timeout=600)

    tags = {
        'craft': 'brewery',
        'industrial': 'brewery',
        'microbrewery': 'yes',
    }

    q = get_query(tags, south, west, north, east)

    response = api.Get(q, asGeoJSON=True)
    features = [parse_brewery(feature) for feature in response['features']]
    return {
        'type': 'featurecollection',
        'features': features
    }


if __name__ == '__main__':
    # bbox = '-12.612305,55.028022,54.140625,71.413177'
    bbox = '10.202522,63.360289,10.724030,63.491452'
    breweries = get_osm_breweries(bbox)
    rb_breweries = read_json('data/rb_breweries.json')

    matcher = BreweryNameMatcher(rb_breweries)
    for brewery in breweries['features']:
        brewery_name = brewery['properties']['name']
        match = matcher.match_name(brewery_name)
        if match is not None:
            print '%s - %s' % (brewery_name, match['name'])
        else:
            print '%s - %s' % (brewery_name, 'NOMATCH')
