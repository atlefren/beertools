# -*- coding: utf-8 -*-

import json

import overpass


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


def get_list_items(tags, condition):
    query = []
    for key, value in tags.iteritems():
        query.append('node[%s=%s](%s)' % (key, value, condition))
        query.append('way[%s=%s](%s)' % (key, value, condition))
        query.append('relation[%s=%s](%s)' % (key, value, condition))
    return ';'.join(query)


def get_query(tags, country=None, south=None, west=None, north=None, east=None):

    if country is not None:
        list_items = get_list_items(tags, 'area.search')
        return 'area["ISO3166-1"="%s"]->.search;(%s)' % (country, list_items)

    bbox = None
    if south is not None and west is not None and north is not None and east is not None:
        bbox = '{south},{west},{north},{east}'.format(
            west=west,
            south=south,
            east=east,
            north=north
        )

    list_items = get_list_items(tags, bbox)
    return '(%s)' % (list_items)


def parse_brewery(feature, country):
    old_properties = feature.get('properties', {})
    properties = {
        'id': feature.get('id', None),
        'id': feature.get('id', None),
        'name': old_properties.get('name', None),
        'housenumber': old_properties.get('addr:housenumber', None),
        'city': old_properties.get('addr:city', None),
        'postcode': old_properties.get('addr:postcode', None),
        'street': old_properties.get('addr:street', None),
        'country': country,
    }

    feature['properties'] = properties
    return feature


def get_osm_breweries(bbox=None, country=None):

    api = overpass.API(timeout=600)

    tags = {
        'craft': 'brewery',
        'industrial': 'brewery',
        'microbrewery': 'yes',
    }

    if bbox is not None:
        south, west, north, east = parse_bbox(bbox)
        q = get_query(tags, south=south, west=west, north=north, east=east)
    elif country is not None:
        q = get_query(tags, country=country)

    if q is None:
        return

    response = api.Get(q, asGeoJSON=True)
    features = [parse_brewery(feature, country) for feature in response['features']]
    return {
        'type': 'featurecollection',
        'features': features
    }


if __name__ == '__main__':
    # bbox = '-12.612305,55.028022,54.140625,71.413177'
    # bbox = '10.202522,63.360289,10.724030,63.491452'
    # breweries = get_osm_breweries(bbox)

    breweries = get_osm_breweries(country='NO')

    with open('data/osm_breweries.geojson', 'w') as outfile:
        outfile.write(json.dumps(breweries, indent=4))
