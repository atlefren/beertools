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

    def test_match_case_differs(self):
        matched = self.matcher_2ol.match_name(u'to øl reparationsbajer')
        self.assertEqual(u'To Øl Reparationsbajer', matched['name'])

    def test_match_with_brewery_name(self):
        matched = self.matcher_2ol.match_name(u'Black Ball Porter')
        self.assertEqual(u'To Øl Black Ball Porter', matched['name'])

    def test_cask_bottle(self):
        beer_list = [
            {'name': u'Hook Norton Haymaker (Cask)'},
            {'name': u'Hook Norton Haymaker (Bottle)'},
        ]

        matcher = BeerNameMatcher(u'Hook Norton', beer_list)

        matched = matcher.match_name(u'Hook Norton Haymaker')
        self.assertEqual(u'Hook Norton Haymaker (Bottle)', matched['name'])

    def test_and(self):
        matched = self.matcher_aegir.match_name(u'Ægir Hrist Og Mist')
        self.assertEqual(u'Ægir Hrist & Mist', matched['name'])

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
        matched = matcher.match_name(u'Big Ben')
        self.assertEqual(u'Thwaites Big Ben (Pasteurized) (2013 - )', matched['name'])

    def test_nora(self):
        beer_list = [
            {'name': u'Baladin Nora Sour Edition'},
            {'name': u'Baladin Nora'},
        ]
        matcher = BeerNameMatcher(u'Le Baladin', beer_list)
        matched = matcher.match_name(u'Baladin Nora 75 cl')
        self.assertEqual(u'Baladin Nora', matched['name'])

    def test_fullers(self):
        beer_list = [
            {'name': u'Fuller’s London Porter (Bottle/Keg)'}
        ]
        matcher = BeerNameMatcher(u'Fuller’s', beer_list)
        matched = matcher.match_name(u'Fuller\'s London Porter')
        self.assertEqual(u'Fuller’s London Porter (Bottle/Keg)', matched['name'])

    def test_proper_job(self):
        beer_list = [
            {'name': u'St. Austell Proper Cool IPA'},
            {'name': u'St. Austell Proper Job (Bottle)'},
        ]
        matcher = BeerNameMatcher(u'St. Austell', beer_list)
        matched = matcher.match_name(u'St. Austell Proper Job IPA')
        self.assertEqual(u'St. Austell Proper Job (Bottle)', matched['name'])

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

    def test_match_beer_type_confusion(self):
        matched = self.matcher_2ol.match_name(u'To Øl Goliat Imperial Stout')
        self.assertEqual(u'To Øl Goliat Imperial Coffee Stout', matched['name'])

    def test_match_beer_and_confusion(self):
        matched = self.matcher_aegir.match_name(u'Ægir Hrist og Mist')
        self.assertEqual(u'Ægir Hrist & Mist', matched['name'])

    def test_match_beer_and_more_types(self):
        matched = self.matcher_aegir.match_name(u'Ægir Hrist Og Mist Hefeweizen')
        self.assertEqual(u'Ægir Hrist & Mist', matched['name'])

    @unittest.skip("")
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

    @unittest.skip("")
    def test_chimay(self):
        beer_list = [
            {'name': u'Chimay (Red / Rouge / Ale / Première)'},
            # {'name': u'Chimay 150 / Spéciale Cent Cinquante'},
            # {'name': u'Chimay Bleue (Blue) / Grande Réserve'},
            # {'name': u'Chimay Dorée / Spéciale du Potaupré '},
            # {'name': u'Chimay Triple / Blanche (White) / Cinq Cents'}
        ]
        matcher = BeerNameMatcher('Chimay', beer_list)

        matched1 = matcher.match_name(u'Chimay Trappist Red Première')
        self.assertEqual(u'Chimay (Red / Rouge / Ale / Première)', matched1['name'])

    @unittest.skip("")
    def test_chimay2(self):
        beer_list = [
            {'name': u'Chimay (Red / Rouge / Ale / Première)'},
            {'name': u'Chimay 150 / Spéciale Cent Cinquante'},
            {'name': u'Chimay Bleue (Blue) / Grande Réserve'},
            {'name': u'Chimay Dorée / Spéciale du Potaupré '},
            {'name': u'Chimay Triple / Blanche (White) / Cinq Cents'}
        ]
        matcher = BeerNameMatcher('Chimay', beer_list)

        matched3 = matcher.match_name(u'Chimay Trappist Red')
        self.assertEqual(u'Chimay (Red / Rouge / Ale / Première)', matched3['name'])

        matched2 = matcher.match_name(u'Chimay Trappist Cinq Cents')
        self.assertEqual(u'Chimay Triple / Blanche (White) / Cinq Cents', matched2['name'])

        matched4 = matcher.match_name(u'Chimay Trappist White')
        self.assertEqual(u'Chimay Triple / Blanche (White) / Cinq Cents', matched4['name'])

        matched5 = matcher.match_name(u'Chimay Trappist Blue 2014')
        self.assertEqual(u'Chimay Bleue (Blue) / Grande Réserve', matched5['name'])

    def test_lokkatrollet(self):
        matcher = BeerNameMatcher(u'Grünerløkka Brygghus', [{'name': u'Grünerløkka Løkkatrollet'}])
        matched = matcher.match_name(u'Grünerløkka Brygghus Løkkatrollet Stout Porter')
        self.assertEqual(u'Grünerløkka Løkkatrollet', matched['name'])

    @unittest.skip("")
    def test_ba_edition(self):
        beer_list = [
            {'name': u'Mikkeller Black Ink And Blood'},
            {'name': u'Mikkeller Black Ink And Blood Barrel Aged (Bourbon Edition)'},
            {'name': u'Mikkeller Black Ink And Blood Barrel Aged (Brandy Edition)'}
        ]

        matcher = BeerNameMatcher(u'Mikkeller', beer_list)
        matched = matcher.match_name(u'Mikkeller Black Ink and Blood Imperial raspberry stout Brandy')
        self.assertEqual(u'Mikkeller Black Ink And Blood Barrel Aged (Brandy Edition)', matched['name'])

    @unittest.skip("")
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

    @unittest.skip("")
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

    def test_emelisse(self):
        beer_list = [
            {'name': u'Emelisse American Pale Ale'},
            {'name': u'Emelisse Double IPA        9%'},
        ]
        matcher = BeerNameMatcher(u'Brouwerij Emelisse', beer_list)
        matched = matcher.match_name(u'Emelisse Double IPA')
        self.assertEqual(u'Emelisse Double IPA        9%', matched['name'])

    def test_unfiltered_synonym(self):
        beer_list = [
            {'name': u'Theresianer Premium Pils'},
            {'name': u'Theresianer Premium Pils Non Filtrata'},
        ]
        matcher = BeerNameMatcher(u'Theresianer Antica Birreria di Trieste', beer_list)
        matched = matcher.match_name(u'Theresianer Premium Pils Unfiltered')
        self.assertEqual(u'Theresianer Premium Pils Non Filtrata', matched['name'])

    def test_unfiltered(self):
        beer_list = [
            {'name': u'Theresianer India Pale Ale'},
            {'name': u'Theresianer Wit'},
        ]
        matcher = BeerNameMatcher(u'Theresianer Antica Birreria di Trieste', beer_list)
        matched = matcher.match_name(u'Theresianer Wit Unfiltered')
        self.assertEqual(u'Theresianer Wit', matched['name'])

    def test_type(self):
        beer_list = [
            {'name': u'Undercover Lager'},
            {'name': u'Undercover Pale Ale'},
        ]
        matcher = BeerNameMatcher(u'Coisbo Beer', beer_list)
        matched = matcher.match_name(u'UnderCover Brewing Pale Ale')
        self.assertEqual(u'Undercover Pale Ale', matched['name'])

    def test_lager_pilsner(self):
        beer_list = [
            {'name': u'Grolsch Amber Ale'},
            {'name': u'Grolsch Premium Lager / Pilsner'},
        ]
        matcher = BeerNameMatcher(u'Grolsche Bierbrouwerij Ned. (SABMiller)', beer_list)
        matched = matcher.match_name(u'Grolsch Premium Lager')
        self.assertEqual(u'Grolsch Premium Lager / Pilsner', matched['name'])

    def test_dash_for_space(self):
        beer_list = [
            {'name': u'Adnams Tally-Ho'},
            {'name': u'Adnams Tally Ho-Ho-Ho'},
        ]
        matcher = BeerNameMatcher(u'Adnams', beer_list)
        matched = matcher.match_name(u'Adnams Tally Ho Ho Ho')
        self.assertEqual(u'Adnams Tally Ho-Ho-Ho', matched['name'])

    def test_abv_limit(self):
        beer_list = [
            {'name': u'Harviestoun Old Engine Oil (4.5%)'},
            {'name': u'Harviestoun Old Engine Oil (Bottle)'},
        ]
        matcher = BeerNameMatcher(u'Harviestoun', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Harviestoun Brewery Old Engine Oil Porter')
        self.assertEqual(u'Harviestoun Old Engine Oil (Bottle)', matched['name'])

    def test_baladin(self):
        beer_list = [
            {'name': u'Baladin NazionAle'},
        ]
        matcher = BeerNameMatcher(u'Le Baladin', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Baladin Nazionale 2012')
        self.assertEqual(u'Baladin NazionAle', matched['name'])

    def test_collab(self):
        beer_list = [
            {'name': u'Nøgne Ø / Terrapin Imperial Rye Porter'},
        ]
        matcher = BeerNameMatcher(u'Nøgne Ø (Hansa Borg)', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Nøgne Ø Imperial Rye Porter')
        self.assertEqual(u'Nøgne Ø / Terrapin Imperial Rye Porter', matched['name'])

    def test_collab_nospace(self):
        beer_list = [
            {'name': u'Amundsen / Garage Project Born Slippy'},
        ]
        matcher = BeerNameMatcher(u'Amundsen Bryggeri & Spiseri', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Garage Project/Amundsen Bryggeri Born Slippy Wheat Beer')
        self.assertEqual(u'Amundsen / Garage Project Born Slippy', matched['name'])

    def test_single_hop(self):
        beer_list = [
            {'name': u'Amundsen One Hop Wonder - Total Eclipse of the hop'},
        ]
        matcher = BeerNameMatcher(u'Amundsen Bryggeri & Spiseri', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Amundsen Total Eclipse of the Hop - Single Hop IPA')
        self.assertEqual(u'Amundsen One Hop Wonder - Total Eclipse of the hop', matched['name'])

    def test_hansa_ipa(self):
        beer_list = [
            {'name': u'Hansa Spesial Porter'},
            {'name': u'Hansa Spesial IPA Extra'},
        ]
        matcher = BeerNameMatcher(u'Hansa Borg Bryggerier', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Hansa IPA Ekstra Spesial')
        self.assertEqual(u'Hansa Spesial IPA Extra', matched['name'])

    def test_cask_vs_filtered(self):
        beer_list = [
            {'name': u'Morland Old Speckled Hen (Cask)'},
            {'name': u'Morland Old Speckled Hen (Cask - 5.2%)'},
            {'name': u'Morland Old Speckled Hen (Filtered)'},
        ]
        matcher = BeerNameMatcher(u'Greene King', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Old Speckled Hen')
        self.assertEqual(u'Morland Old Speckled Hen (Filtered)', matched['name'])

    def test_special_blend(self):
        beer_list = [
            {'name': u'Lindemans Oude Gueuze Cuvée René Special Blend 2010'},
            {'name': u'Lindemans Gueuze Cuvée René'},
        ]
        matcher = BeerNameMatcher(u'Brouwerij Lindemans', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Lindemans Oude Gueuze Cuvée René')
        self.assertEqual(u'Lindemans Gueuze Cuvée René', matched['name'])

    def test_brown_bruin(self):
        beer_list = [
            {'name': u'Maredsous 6 Blond'},
            {'name': u'Maredsous 8 Brune/Bruin'},
        ]
        matcher = BeerNameMatcher(u'Duvel Moortgat', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Maredsous Brown')
        self.assertEqual(u'Maredsous 8 Brune/Bruin', matched['name'])

    def test_abv_and_cask2(self):
        beer_list = [
            {'name': u'Shepherd Neame Double Stout (5.2% - Bottle)'},
            {'name': u'Shepherd Neame Double Stout (5.2% - Cask)'},
        ]
        matcher = BeerNameMatcher(u'Shepherd Neame', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Shepherd Neame Double Stout')
        self.assertEqual(u'Shepherd Neame Double Stout (5.2% - Bottle)', matched['name'])

    def test_bitburger(self):
        beer_list = [
            {'name': u'Bitburger Premium Pils'},
        ]
        matcher = BeerNameMatcher(u'Bitburger Brauerei Th. Simon', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Bitburger Premium')
        self.assertEqual(u'Bitburger Premium Pils', matched['name'])

    def test_okologisk(self):
        beer_list = [
            {'name': u'Herslev Økologisk Pale Ale'},
        ]
        matcher = BeerNameMatcher(u'Herslev Bryghus', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Herslev Bryghus Pale Ale')
        self.assertEqual(u'Herslev Økologisk Pale Ale', matched['name'])

    def test_hefeweizen(self):
        beer_list = [
            {'name': u'Erdinger Weissbier (Hefe-Weizen)'},
        ]
        matcher = BeerNameMatcher(u'Erdinger Weissbräu', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Erdinger Weissbier')
        self.assertEqual(u'Erdinger Weissbier (Hefe-Weizen)', matched['name'])

    def test_dunkel_dark(self):
        beer_list = [
            {'name': u'Erdinger Weissbier Hefe-Weizen Dark'},
        ]
        matcher = BeerNameMatcher(u'Erdinger Weissbräu', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Erdinger Weissbier Dunkel')
        self.assertEqual(u'Erdinger Weissbier Hefe-Weizen Dark', matched['name'])

    def test_parentesis(self):
        beer_list = [
            {'name': u'Nøgne Ø Lemongrass (Aku Aku Lemongrass Ale)'},
        ]
        matcher = BeerNameMatcher(u'Nøgne Ø (Hansa Borg)', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Nøgne Ø Lemongrass')
        self.assertEqual(u'Nøgne Ø Lemongrass (Aku Aku Lemongrass Ale)', matched['name'])
