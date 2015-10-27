# -*- coding: utf-8 -*-

import unittest

from beernamematcher import BeerNameMatcher

BEERS_2OL = [
    {'name': u'To Øl Reparationsbajer'},
    {'name': u'To Øl Goliat Imperial Coffee Stout'},
    {'name': u'To Øl Black Ball Porter'},
    {'name': u'Shivity IPA'},
]

BEERS_AEGIR = [
    {'name': u'Ægir Hrist & Mist'},
    {'name': u'Ægir Lynchburg Natt'},
    {'name': u'Ægir Skjeggjøld'}
]


class BeerNameMatcherTest(unittest.TestCase):

    def setUp(self):
        self.matcher_2ol = BeerNameMatcher(u'To Øl', BEERS_2OL)
        self.matcher_aegir = BeerNameMatcher(u'Ægir Bryggeri', BEERS_AEGIR)

    def test_match_similar(self):
        matched = self.matcher_2ol.match_name(u'Shivity IPA')
        self.assertEqual(u'Shivity IPA', matched['name'])

    def test_match_with_brewery_name(self):
        matched = self.matcher_2ol.match_name(u'Black Ball Porter')
        self.assertEqual(u'To Øl Black Ball Porter', matched['name'])

    def test_match_case_differs(self):
        matched = self.matcher_2ol.match_name(u'to øl reparationsbajer')
        self.assertEqual(u'To Øl Reparationsbajer', matched['name'])

    def test_match_beer_type_confusion(self):
        matched = self.matcher_2ol.match_name(u'To Øl Goliat Imperial Stout')
        self.assertEqual(u'To Øl Goliat Imperial Coffee Stout', matched['name'])

    def test_match_beer_and_confusion(self):
        matched = self.matcher_aegir.match_name(u'Ægir Hrist og Mist')
        self.assertEqual(u'Ægir Hrist & Mist', matched['name'])

    def test_match_beer_and_more_types(self):
        matched = self.matcher_aegir.match_name(u'Ægir Hrist Og Mist Hefeweizen')
        self.assertEqual(u'Ægir Hrist & Mist', matched['name'])

    def test_match_several_types(self):
        matched = self.matcher_aegir.match_name(u'Ægir Lynchburg Natt Barrel-Aged Imperial Porter')
        self.assertEqual(u'Ægir Lynchburg Natt', matched['name'])

    def test_match_india_red(self):
        matched = self.matcher_aegir.match_name(u'Ægir Skjeggjøld India Red Ale')
        self.assertEqual(u'Ægir Skjeggjøld', matched['name'])

    def test_match_humlehelvete(self):
        matcher = BeerNameMatcher('Bryggerhuset Veholt', [{'name': u'Veholt Humlehelvete'}])
        matched = matcher.match_name(u'Veholt Humlehelvete Double IPA Originalen')
        self.assertEqual(u'Veholt Humlehelvete', matched['name'])

    def test_match_putin(self):
        matcher = BeerNameMatcher('Indslev Bryggeri', [{'name': u'Ugly Duck Putin'}])
        matched = matcher.match_name(u'Ugly Duck Putin Imperial Wheat Stout')
        self.assertEqual(u'Ugly Duck Putin', matched['name'])

    def test_chimay(self):
        beer_list = [
            {'name': u'Chimay (Red / Rouge / Ale / Première)'},
            {'name': u'Chimay 150 / Spéciale Cent Cinquante'},
            {'name': u'Chimay Bleue (Blue) / Grande Réserve'},
            {'name': u'Chimay Dorée / Spéciale du Potaupré '},
            {'name': u'Chimay Triple / Blanche (White) / Cinq Cents'}
        ]
        matcher = BeerNameMatcher('Chimay', beer_list)

        matched1 = matcher.match_name(u'Chimay Trappist Red Première')
        self.assertEqual(u'Chimay (Red / Rouge / Ale / Première)', matched1['name'])

        matched2 = matcher.match_name(u'Chimay Trappist Cinq Cents')
        self.assertEqual(u'Chimay Triple / Blanche (White) / Cinq Cents', matched2['name'])

        matched3 = matcher.match_name(u'Chimay Trappist Red')
        self.assertEqual(u'Chimay (Red / Rouge / Ale / Première)', matched3['name'])

        matched4 = matcher.match_name(u'Chimay Trappist White')
        self.assertEqual(u'Chimay Triple / Blanche (White) / Cinq Cents', matched4['name'])

        matched5 = matcher.match_name(u'Chimay Trappist Blue 2014')
        self.assertEqual(u'Chimay Bleue (Blue) / Grande Réserve', matched5['name'])

    def test_lokkatrollet(self):
        matcher = BeerNameMatcher(u'Grünerløkka Brygghus', [{'name': u'Grünerløkka Løkkatrollet'}])
        matched = matcher.match_name(u'Grünerløkka Brygghus Løkkatrollet Stout Porter')
        self.assertEqual(u'Grünerløkka Løkkatrollet', matched['name'])

    @unittest.skip('not solved yet')
    def test_ba_edition(self):
        beer_list = [
            {'name': u'Mikkeller Black Ink And Blood'},
            {'name': u'Mikkeller Black Ink And Blood Barrel Aged (Bourbon Edition)'},
            {'name': u'Mikkeller Black Ink And Blood Barrel Aged (Brandy Edition)'}
        ]

        matcher = BeerNameMatcher(u'Mikkeller', beer_list)
        matched = matcher.match_name(u'Mikkeller Black Ink and Blood Imperial raspberry stout Brandy')
        self.assertEqual(u'Mikkeller Black Ink And Blood Barrel Aged (Brandy Edition)', matched['name'])

    @unittest.skip('not solved yet')
    def test_rye_ipa(self):
        beer_list = [
            {'name': u'Adnams Oak Aged IPA'},
            {'name': u'Adnams Jack Brand Crystal Rye IPA'},
        ]

        matcher = BeerNameMatcher(u'Adnams', beer_list)
        matched = matcher.match_name(u'Adnams Rye IPA')
        self.assertEqual(u'Adnams Jack Brand Crystal Rye IPA', matched['name'])

    def test_ipa_apa(self):
        beer_list = [
            {'name': u'Lervig APA'},
            {'name': u'Lervig Brewers Reserve Galaxy IPA Single Hopped'},
        ]

        matcher = BeerNameMatcher(u'Lervig Aktiebryggeri', beer_list)
        matched = matcher.match_name(u'Lervig Galaxy IPA')
        self.assertEqual(u'Lervig Brewers Reserve Galaxy IPA Single Hopped', matched['name'])

    @unittest.skip('not solved yet')
    def test_white_ipa(self):

        beer_list = [
            {'name': u'Lervig Brewers Reserve Oat IPA'},
            {'name': u'Lervig Brewers Reserve White IPA Wit & IPA Fusion'},
        ]

        matcher = BeerNameMatcher(u'Lervig Aktiebryggeri', beer_list)
        matched = matcher.match_name(u'Lervig Brewers Reserve White IPA')
        self.assertEqual(u'Lervig Brewers Reserve White IPA Wit & IPA Fusion', matched['name'])

    def test_la_trappe(self):
        beer_list = [
            {'name': u'La Trappe Witte Trappist'},
            {'name': u'La Trappe Blond'},
            {'name': u'La Trappe Isid’or'},
            {'name': u'La Trappe Tripel'},
            {'name': u'La Trappe Bockbier'},
            {'name': u'La Trappe Dubbel'},

        ]

        matcher = BeerNameMatcher(u'De Koningshoeven (Bavaria - Netherlands)', beer_list)

        matched = matcher.match_name(u'La Trappe Blond Trappist')
        self.assertEqual(u'La Trappe Blond', matched['name'])

        matched = matcher.match_name(u'La Trappe Isid\'or Trappist')
        self.assertEqual(u'La Trappe Isid’or', matched['name'])

        matched = matcher.match_name(u'La Trappe Tripel Trappist ')
        self.assertEqual(u'La Trappe Tripel', matched['name'])

        matched = matcher.match_name(u'La Trappe Dubbel Trappist')
        self.assertEqual(u'La Trappe Dubbel', matched['name'])

        matched = matcher.match_name(u'La Trappe Bockbier Trappistenbier')
        self.assertEqual(u'La Trappe Bockbier', matched['name'])

    def test_rochefort(self):
        beer_list = [
            {'name': u'Rochefort Trappistes 6'},
            {'name': u'Rochefort Trappistes 10'},
            {'name': u'Rochefort Trappistes 8'},
            {'name': u'La Trappe Tripel'},
            {'name': u'La Trappe Bockbier'},
            {'name': u'La Trappe Dubbel'},

        ]

        matcher = BeerNameMatcher(u'Brasserie Rochefort', beer_list)

        matched = matcher.match_name(u'Rochefort 10 Trappist')
        self.assertEqual(u'Rochefort Trappistes 10', matched['name'])

        matched = matcher.match_name(u'Rochefort 8 Trappist')
        self.assertEqual(u'Rochefort Trappistes 8', matched['name'])

    def test_noisom(self):
        beer_list = [
            {'name': u'Nøisom Brown Ale'},
            {'name': u'Nøisom Somnus'}

        ]

        matcher = BeerNameMatcher(u'Nøisom Craft Beer', beer_list)

        matched = matcher.match_name(u'Nøisom Somnus Brown Ale')
        self.assertEqual(u'Nøisom Somnus', matched['name'])

    def test_cask_bottle(self):
        beer_list = [
            {'name': u'Hook Norton Haymaker (Cask)'},
            {'name': u'Hook Norton Haymaker (Bottle)'},
        ]

        matcher = BeerNameMatcher(u'Hook Norton', beer_list)

        matched = matcher.match_name(u'Hook Norton Haymaker')
        self.assertEqual(u'Hook Norton Haymaker (Bottle)', matched['name'])

    def test_cask_keg_bottle(self):
        beer_list = [
            {'name': u'Harviestoun Schiehallion (Cask)'},
            {'name': u'Harviestoun Schiehallion (Bottle/Keg)'},
        ]

        matcher = BeerNameMatcher(u'Harviestoun', beer_list)

        matched = matcher.match_name(u'Harviestoun Schiehallion Craft Lager')
        self.assertEqual(u'Harviestoun Schiehallion (Bottle/Keg)', matched['name'])

    def test_cask_pasteurized(self):
        beer_list = [
            {'name': u'Thwaites Big Ben (Cask)'},
            # {'name': u'Thwaites Big Ben (Pasteurised) (up to 2013)'},
            {'name': u'Thwaites Big Ben (Pasteurized)'},
        ]

        matcher = BeerNameMatcher(u'Thwaites', beer_list)

        matched = matcher.match_name(u'Big Ben Brown Ale')
        self.assertEqual(u'Thwaites Big Ben (Pasteurized)', matched['name'])

    def test_by_the_horns(self):
        beer_list = [
            {'name': u'By The Horns Lambeth Walk (Vanilla Whiskey Special)'},
            {'name': u'By The Horns Lambeth Walk'},
        ]
        matcher = BeerNameMatcher(u'By The Horns', beer_list)
        matched = matcher.match_name(u'By The Horns Lambeth Walk London Porter')
        self.assertEqual(u'By The Horns Lambeth Walk', matched['name'])

    def test_harviestoun(self):
        beer_list = [
            {'name': u'Harviestoun Old Engine Oil Special Reserve (10.5 %)'},
            {'name': u'Harviestoun Old Engine Oil (Bottle)'},
        ]
        matcher = BeerNameMatcher(u'Harviestoun', beer_list)
        matched = matcher.match_name(u'Harviestoun Brewery Old Engine Oil Porter')
        self.assertEqual(u'Harviestoun Old Engine Oil (Bottle)', matched['name'])

    def test_nora(self):
        beer_list = [
            {'name': u'Baladin Nora Sour Edition'},
            {'name': u'Baladin Nora'},
        ]
        matcher = BeerNameMatcher(u'Le Baladin', beer_list)
        matched = matcher.match_name(u'Baladin Nora 75 cl')
        self.assertEqual(u'Baladin Nora', matched['name'])

    def test_percentage(self):
        beer_list = [
            {'name': u'BrewDog Punk Pale Ale'},
            {'name': u'BrewDog Punk IPA (5.6%)'},
        ]
        matcher = BeerNameMatcher(u'BrewDog', beer_list)
        matched = matcher.match_name(u'BrewDog Punk IPA')
        self.assertEqual(u'BrewDog Punk IPA (5.6%)', matched['name'])

    def test_year(self):
        beer_list = [
            {'name': u'Thwaites Big Ben (Cask)'},
            {'name': u'Thwaites Big Ben (Pasteurized) (2013 - )'},
        ]
        matcher = BeerNameMatcher(u'Thwaites', beer_list)
        matched = matcher.match_name(u'Big Ben Brown Ale')
        self.assertEqual(u'Thwaites Big Ben (Pasteurized) (2013 - )', matched['name'])

    def test_proper_job(self):
        beer_list = [
            {'name': u'St. Austell Proper Cool IPA'},
            {'name': u'St. Austell Proper Job (Bottle)'},
        ]
        matcher = BeerNameMatcher(u'St. Austell', beer_list)
        matched = matcher.match_name(u'St. Austell Proper Job IPA')
        self.assertEqual(u'St. Austell Proper Job (Bottle)', matched['name'])

    def test_fullers(self):
        beer_list = [
            {'name': u'Fuller’s London Porter (Bottle/Keg)'}
        ]
        matcher = BeerNameMatcher(u'Fuller’s', beer_list)
        matched = matcher.match_name(u'Fuller\'s London Porter')
        self.assertEqual(u'Fuller’s London Porter (Bottle/Keg)', matched['name'])
