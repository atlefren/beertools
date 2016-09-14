# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def parse_soup(html):
    updated = datetime.now()
    soup = BeautifulSoup(html, 'html.parser')
    pol_list = soup.findAll('li', {'class': 'product-item'})
    results = []
    stock_regexp = re.compile(u': (\d+) på lager$')
    id_regexp = re.compile(u'/p/(.*)$')
    for item in pol_list:
        stock_div = item.find('div', {'class': 'product-stock-status'}).findChildren()[1]
        stock_text = stock_div.text.strip()
        stock_res = stock_regexp.search(stock_text)
        stock = 0
        if stock_res is not None:
            stock = int(stock_res.group(1))
        id_url = item.find('h2', {'class': 'product-item__name'}).find('a').attrs['href']
        id_res = id_regexp.search(id_url)
        shop_id = None
        if id_res is not None:
            shop_id = int(id_res.group(1))
        if shop_id is not None:
            results.append({
                'pol_id': shop_id,
                'stock': stock,
                'updated': updated
            })

    return results


def get_page(pol_id, page):
    url = u'https://www.vinmonopolet.no/vmpSite/search?q=:relevance:availableInStores:%s:visibleInSearch:true:mainCategory:øl&page=%s&searchType=' % (pol_id, page)
    r = requests.get(url)
    return parse_soup(r.text)


def get_pol_stock_for_pol(pol_id):
    next_page = True
    page = 0
    results = []
    while next_page:
        stock = get_page(pol_id, page)
        if len(stock) == 0:
            next_page = False
        results += stock
        page += 1
    return results


if __name__ == '__main__':
    print get_pol_stock_for_pol(180)
