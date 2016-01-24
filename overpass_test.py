# -*- coding: utf-8 -*-

import json

import overpass


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


def get_osm_breweries(country_code):
    api = overpass.API(timeout=600)

    q = '''
    area["ISO3166-1"="%s"]->.search;
    (
      node[industrial=brewery](area.search);
      node[microbrewery=yes](area.search);
      node[craft=brewery](area.search);
      way[industrial=brewery](area.search);
      way[microbrewery=yes](area.search);
      way[craft=brewery](area.search);
      relation[industrial=brewery](area.search);
      relation[microbrewery=yes](area.search);
      relation[craft=brewery](area.search);
    );''' % country_code

    response = api.Get(q)
    features = [parse_brewery(feature) for feature in response['features']]
    return {
        'type': 'featurecollection',
        'features': features
    }


if __name__ == '__main__':
    breweries = get_osm_breweries('NO')
    print breweries
    with open('breweries.geojson', 'w') as out:
        out.write(json.dumps(breweries))
