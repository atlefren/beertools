# -*- coding: utf-8 -*-
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def parse_soup(html):
    soup = BeautifulSoup(html, 'html.parser')
    pol_list = soup.find('div', {'class': 'listStores'})
    if pol_list is None:
        return []
    regexp = re.compile('\?butikk_id=(.*)$')
    data = []
    for pol in pol_list.findAll('li'):
        span = pol.find('em').find('span')
        pol_id = pol.find('a').attrs['href']
        updated = span.attrs['title'].replace('Oppdatert ', '')
        data.append({
            'pol_id': regexp.search(pol_id).group(1),
            'pol_name': pol.find('strong').text,
            'stock': int(span.text.replace(u'på lager)', '').replace('(', '').replace('.', '')),
            'updated': datetime.strptime(updated, '%d.%m.%Y %H:%M:%S') if updated is not None else None
        })
    return data


def check_beer(varenr):
    url = 'http://www.vinmonopolet.no/vareutvalg/0/0/0/sku-{0}?ShowShopsWithProdInStock=true&sku={0}&fylke_id=*'
    r = requests.get(url.format(varenr))
    return parse_soup(r.text)


if __name__ == '__main__':
    print check_beer('1858602')
