# -*- coding: utf-8 -*-
import overpass
from shapely.geometry import mapping, shape, Polygon


def find_center(geometry):
    s = shape(geometry)
    s.coords
    return mapping(Polygon(s.coords).centroid)


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

    if feature['geometry']['type'] == 'LineString':
        feature['geometry'] = find_center(feature['geometry'])

    return feature


def get_list_items(tags, condition):
    query = []
    for key, value in tags.iteritems():
        query.append('node[%s=%s](%s)' % (key, value, condition))
        query.append('way[%s=%s](%s)' % (key, value, condition))
        query.append('relation[%s=%s](%s)' % (key, value, condition))
    return ';'.join(query)


def get_query(country, tags):
    list_items = get_list_items(tags, 'area.search')
    return 'area["ISO3166-1"="%s"]->.search;(%s)' % (country, list_items)


def get_osm_breweries(country):

    tags = {
        'craft': 'brewery',
        'industrial': 'brewery',
        'microbrewery': 'yes',
    }
    q = get_query(country, tags)

    api = overpass.API(timeout=600)
    response = api.Get(q, responseformat='geojson')
    features = [parse_brewery(feature, country)
                for feature in response['features']]
    return {
        'type': 'featurecollection',
        'features': features
    }

if __name__ == '__main__':
    breweries = get_osm_breweries('NO')
    for b in breweries['features']:
        print b
