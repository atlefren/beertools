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

    @unittest.skip("")
    def test_rye_ipa(self):
        beer_list = [
            {'name': u'Adnams Oak Aged IPA'},
            {'name': u'Adnams Jack Brand Crystal Rye IPA'},
        ]

        matcher = BeerNameMatcher(u'Adnams', beer_list)
        matched = matcher.match_name(u'Adnams Rye IPA')
        self.assertEqual(u'Adnams Jack Brand Crystal Rye IPA', matched['name'])

    @unittest.skip("")
    def test_white_ipa(self):

        beer_list = [
            {'name': u'Lervig Brewers Reserve Oat IPA'},
            {'name': u'Lervig Brewers Reserve White IPA Wit & IPA Fusion'},
        ]

        matcher = BeerNameMatcher(u'Lervig Aktiebryggeri', beer_list)
        matched = matcher.match_name(u'Lervig Brewers Reserve White IPA')
        self.assertEqual(u'Lervig Brewers Reserve White IPA Wit & IPA Fusion', matched['name'])

    @unittest.skip("")
    def test_pilsen(self):
        beer_list = [
            {'name': u'Efes Pilsen Unfiltered'},
            {'name': u'Efes Pilsen (Pilsener)'}
        ]
        matcher = BeerNameMatcher(u'Anadolu Efes', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Efes Pilsner')
        self.assertEqual(u'Efes Pilsen (Pilsener)', matched['name'])

    @unittest.skip("")
    def test_staropramen(self):
        beer_list = [
            {'name': u'Staropramen Unfiltered'},
            {'name': u'Staropramen Premium Lager'}
        ]
        matcher = BeerNameMatcher(u'Staropramen Breweries (MolsonCoors)', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Staropramen')
        self.assertEqual(u'Staropramen Premium Lager', matched['name'])

    @unittest.skip("")
    def test_baladin_super(self):
        beer_list = [
            {'name': u'Baladin Super 9°'},
            {'name': u'Baladin Super Baladin'}
        ]
        matcher = BeerNameMatcher(u'Le Baladin', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Baladin Super')
        self.assertEqual(u'Baladin Super Baladin', matched['name'])

    @unittest.skip("")
    def test_imperial_pils(self):
        beer_list = [
            {'name': u'Jihlavský Grand 18°'}
        ]
        matcher = BeerNameMatcher(u'Pivovar Jihlava (Pivovary Lobkowicz)', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Pivovar Jihlava Grand Imperial Pils')
        self.assertEqual(u'Jezek Grand Pilsner', matched['name'])

    @unittest.skip("")
    def test_pils_wit(self):
        beer_list = [
            {'name': u'Mikkeller Vesterbro Pilsner', },
            {'name': u'Mikkeller Vesterbro Wit', 'abv': 4.5}
        ]
        matcher = BeerNameMatcher(u'Mikkeller', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Mikkeller Vesterbro Wit')
        self.assertEqual(u'Mikkeller Vesterbro Wit', matched['name'])

    @unittest.skip("")
    def test_batch_100(self):
        beer_list = [
            {'name': u'Nøgne Ø # 1001'},
            {'name': u'Nøgne Ø # 100 (Batch 100)'}
        ]
        matcher = BeerNameMatcher(u'Nøgne Ø (Hansa Borg)', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Nøgne Ø # 100')
        self.assertEqual(u'Nøgne Ø # 100 (Batch 100)', matched['name'])

    @unittest.skip("")
    def test_bons_voeux(self):
        beer_list = [
            {'name': u'Dupont Avec les Bons Voeux'}
        ]
        matcher = BeerNameMatcher(u'Brasserie Dupont', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Dupont Bons Væux')
        self.assertEqual(u'Dupont Avec les Bons Voeux', matched['name'])

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



    def test_lokkatrollet(self):
        matcher = BeerNameMatcher(u'Grünerløkka Brygghus', [{'name': u'Grünerløkka Løkkatrollet'}])
        matched = matcher.match_name(u'Grünerløkka Brygghus Løkkatrollet Stout Porter')
        self.assertEqual(u'Grünerløkka Løkkatrollet', matched['name'])

    def test_ba_edition(self):
        beer_list = [
            {'name': u'Mikkeller Black Ink And Blood'},
            {'name': u'Mikkeller Black Ink And Blood Barrel Aged (Bourbon Edition)'},
            {'name': u'Mikkeller Black Ink And Blood Barrel Aged (Brandy Edition)'}
        ]

        matcher = BeerNameMatcher(u'Mikkeller', beer_list)
        matched = matcher.match_name(u'Mikkeller Black Ink and Blood Imperial raspberry stout Brandy')
        self.assertEqual(u'Mikkeller Black Ink And Blood Barrel Aged (Brandy Edition)', matched['name'])

    def test_ipa_apa(self):
        beer_list = [
            {'name': u'Lervig APA'},
            {'name': u'Lervig Brewers Reserve Galaxy IPA Single Hopped'},
        ]

        matcher = BeerNameMatcher(u'Lervig Aktiebryggeri', beer_list)
        matched = matcher.match_name(u'Lervig Galaxy IPA')
        self.assertEqual(u'Lervig Brewers Reserve Galaxy IPA Single Hopped', matched['name'])

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

    def test_pils_pilsner(self):
        beer_list = [
            {'name': u'Mikkeller Vesterbro Pale Ale'},
            {'name': u'Mikkeller Vesterbro Pilsner'},
        ]
        matcher = BeerNameMatcher(u'Mikkeller', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Mikkeller Vesterbro Pils')
        self.assertEqual(u'Mikkeller Vesterbro Pilsner', matched['name'])

    def test_ipa_abbrev(self):
        beer_list = [
            {'name': u'Midtfyns Double India Pale Ale (Coop Grill)'},
            {'name': u'Midtfyns Double IPA'},
        ]
        matcher = BeerNameMatcher(u'Midtfyns Bryghus', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Midtfyns Bryghus Double India Pale Ale')
        self.assertEqual(u'Midtfyns Double IPA', matched['name'])

    def test_noir(self):
        beer_list = [
            {'name': u'Verhaeghe Barbe d’Or'},
            {'name': u'Verhaeghe Barbe Noire (Barbe Black)'},
        ]
        matcher = BeerNameMatcher(u'Verhaeghe', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Verhaeghe Barbe Noir')
        self.assertEqual(u'Verhaeghe Barbe Noire (Barbe Black)', matched['name'])

    def test_sara(self):
        beer_list = [
            {'name': u'Silenrieux Sara Blonde (Biologique)'}
        ]
        matcher = BeerNameMatcher(u'Silenrieux', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Sara de Silenrieux Bio')
        self.assertEqual(u'Silenrieux Sara Blonde (Biologique)', matched['name'])

    def test_sierra_nevada(self):
        beer_list = [
            {'name': u'Sierra Nevada Pale Ale (Bottle/Can)'}
        ]
        matcher = BeerNameMatcher(u'Sierra Nevada Brewing Company', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Sierra Nevada Pale Ale')
        self.assertEqual(u'Sierra Nevada Pale Ale (Bottle/Can)', matched['name'])

    def test_rye_ipa2(self):
        beer_list = [
            {'name': u'Beavertown 8 Ball'}
        ]
        matcher = BeerNameMatcher(u'Beavertown', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Beavertown 8 Ball Rye IPA')
        self.assertEqual(u'Beavertown 8 Ball', matched['name'])

    def test_dubbel_wit(self):
        beer_list = [
            {'name': u'Glazen Toren Jan De Lichte'}
        ]
        matcher = BeerNameMatcher(u'Kleinbrouwerij De Glazen Toren', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Glazen Toren Jan de Lichte Dubbel Witbier')
        self.assertEqual(u'Glazen Toren Jan De Lichte', matched['name'])

    def test_triple(self):
        beer_list = [
            {'name': u'Paix Dieu Triple'}
        ]
        matcher = BeerNameMatcher(u'Caulier', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Paix Dieu')
        self.assertEqual(u'Paix Dieu Triple', matched['name'])

    def test_dunkles_weizen(self):
        beer_list = [
            {'name': u'Coisbo Pinnekjøttøl Dunkles Weizen'}
        ]
        matcher = BeerNameMatcher(u'Coisbo Beer', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Coisbo Weissbier Pinnekjøt-øl')
        self.assertEqual(u'Coisbo Pinnekjøttøl Dunkles Weizen', matched['name'])

    def test_apostrophe(self):
        beer_list = [
            {'name': u'Fuller’s 1845'}
        ]
        matcher = BeerNameMatcher(u'Fuller’s', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Fuller`s 1845')
        self.assertEqual(u'Fuller’s 1845', matched['name'])

    def test_marstons(self):
        beer_list = [
            {'name': u'Marstons Old Empire (Bottle)'}
        ]
        matcher = BeerNameMatcher(u'Marstons', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Marston\'s Old Empire IPA')
        self.assertEqual(u'Marstons Old Empire (Bottle)', matched['name'])

    def test_lagerol(self):
        beer_list = [
            {'name': u'Rådanäs Lageröl'}
        ]
        matcher = BeerNameMatcher(u'Rådanäs Bryggeri', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Rådanäs Lager')
        self.assertEqual(u'Rådanäs Lageröl', matched['name'])

    def test_oyster_stout(self):
        beer_list = [
            {'name': u'Ægir / Garage Project First Wave'}
        ]
        matcher = BeerNameMatcher(u'Ægir Bryggeri', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Garage Project/Ægir Bryggeri First Wave Oyster Stout')
        self.assertEqual(u'Ægir / Garage Project First Wave', matched['name'])

    def test_parenthesis(self):
        beer_list = [
            {'name': u'Flying Dog Snake Dog IPA (Raspberry Puree & Orange Peel)'},
            {'name': u'Flying Dog Snake Dog IPA (2008 and later)'}
        ]
        matcher = BeerNameMatcher(u'Flying Dog Brewery', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Flying Dog Snake Dog IPA')
        self.assertEqual(u'Flying Dog Snake Dog IPA (2008 and later)', matched['name'])

    def test_sorting(self):
        beer_list = [
            {'name': u'CAP Jernteppet Hammerfest'}
        ]
        matcher = BeerNameMatcher(u'CAP Brewery', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'CAP Hammerfest Jernteppet Pale Ale')
        self.assertEqual(u'CAP Jernteppet Hammerfest', matched['name'])

    def test_hanssens(self):
        beer_list = [
            {'name': u'Hanssens Oude Schaarbeekse Kriek'}
        ]
        matcher = BeerNameMatcher(u'Hanssens Artisanaal', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Hanssens Oude Kriek Handgeplukte Schaerbeekske Krieken')
        self.assertEqual(u'Hanssens Oude Schaarbeekse Kriek', matched['name'])

    def test_borgo(self):
        beer_list = [
            {'name': u'Birra del Borgo Re Ale'}
        ]
        matcher = BeerNameMatcher(u'Birra del Borgo', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Birra del Borga ReAle')
        self.assertEqual(u'Birra del Borgo Re Ale', matched['name'])

    def test_spaces(self):
        beer_list = [
            {'name': u'Beer Here Angry Hops'}
        ]
        matcher = BeerNameMatcher(u'Beer Here', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Beerhere Angry Hops IPA')
        self.assertEqual(u'Beer Here Angry Hops', matched['name'])

    def test_hook_norton(self):
        beer_list = [
            {'name': u'Hook Norton - Hook Norton Flagship (Keg)'},
            {'name': u'Hook Norton - Hook Norton Flagship (Cask & Bottle Conditioned)'}
        ]
        matcher = BeerNameMatcher(u'Hook Norton', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Hook Norton Flagship')
        self.assertEqual(u'Hook Norton - Hook Norton Flagship (Cask & Bottle Conditioned)', matched['name'])

    def test_fantome(self):
        beer_list = [
            {'name': u'Fantôme India Red Ale (IRA)'}
        ]
        matcher = BeerNameMatcher(u'Brasserie Fantôme', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Brasserie Fantome India Red Ale')
        self.assertEqual(u'Fantôme India Red Ale (IRA)', matched['name'])

    def test_pater(self):
        beer_list = [
            {'name': u'Corsendonk Pater / Abbey Brown Ale'}
        ]
        matcher = BeerNameMatcher(u'Brouwerij Corsendonk', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Corsendonk Pater Dubbel')
        self.assertEqual(u'Corsendonk Pater / Abbey Brown Ale', matched['name'])

    def test_messy_rye(self):
        beer_list = [
            {'name': u'Nøisom Messy Rye'}
        ]
        matcher = BeerNameMatcher(u'Nøisom Craft Beer', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Nøisom Messy Rye Rug IPA')
        self.assertEqual(u'Nøisom Messy Rye', matched['name'])

    def test_premium_pils(self):
        beer_list = [
            {'name': u'Lederer Premium Pils'}
        ]
        matcher = BeerNameMatcher(u'Tucher Bräu Fürth (Oetker Group)', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Lederer Pils')
        self.assertEqual(u'Lederer Premium Pils', matched['name'])

    def test_mini_keg(self):
        beer_list = [
            {'name': u'Früh Kölsch'}
        ]
        matcher = BeerNameMatcher(u'Cölner Hofbräu P. Josef Früh', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Früh Kölsch Mini Keg')
        self.assertEqual(u'Früh Kölsch', matched['name'])

    def test_seasonal(self):
        beer_list = [
            {'name': u'Mohawk Whiteout Imperial Stout'}
        ]
        matcher = BeerNameMatcher(u'Mohawk Brewing Company', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Mohawk Whiteout Seasonal Imperial Stout')
        self.assertEqual(u'Mohawk Whiteout Imperial Stout', matched['name'])

    def test_herb(self):
        beer_list = [
            {'name': u'Szigeti Beer'}
        ]
        matcher = BeerNameMatcher(u'Sektkellerei Gebrüder Szigeti', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Szigeti Beer Herb')
        self.assertEqual(u'Szigeti Beer', matched['name'])

    def test_lervig_rye_ipa(self):
        beer_list = [
            {'name': u'Lervig Brewers Reserve Rye IPA - Barrel Aged'},
            {'name': u'Lervig Brewers Reserve Rye IPA'}
        ]
        matcher = BeerNameMatcher(u'Lervig Aktiebryggeri', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Lervig Rye IPA')
        self.assertEqual(u'Lervig Brewers Reserve Rye IPA', matched['name'])

    def test_electric_nurse(self):
        beer_list = [
            {'name': u'Electric Nurse DIPA'}
        ]
        matcher = BeerNameMatcher(u'Dugges Ale & Porterbryggeri', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Electric Nurse DIPA')
        self.assertEqual(u'Electric Nurse DIPA', matched['name'])

    def test_semicolon(self):
        beer_list = [
            {'name': u'Fantôme Artist: Gaelle Boulanger'}
        ]
        matcher = BeerNameMatcher(u'Brasserie Fantôme ', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Fantome Artist')
        self.assertEqual(u'Fantôme Artist: Gaelle Boulanger', matched['name'])

    def test_ambree(self):
        beer_list = [
            {'name': u'Abbaye des Rocs La Montagnarde (Ambree)'}
        ]
        matcher = BeerNameMatcher(u'Brasserie de l’Abbaye des Rocs', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Abbaye des Rocs Montagnarde')
        self.assertEqual(u'Abbaye des Rocs La Montagnarde (Ambree)', matched['name'])

    def test_shepard_neame(self):
        beer_list = [
            {'name': u'Shepherd Neame Double Stout (5.2% - Cask)'},
            {'name': u'Shepherd Neame Double Stout (5.2% - Bottle)'}
        ]
        matcher = BeerNameMatcher(u'Shepherd Neame', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Shepherd Neame Double Stout')
        self.assertEqual(u'Shepherd Neame Double Stout (5.2% - Bottle)', matched['name'])

    def test_red_hopster(self):
        beer_list = [
            {'name': u'Lindheim Red Hopster'}
        ]
        matcher = BeerNameMatcher(u'Lindheim Ølkompani', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Lindheim Red Hopster Imperial Red Ale')
        self.assertEqual(u'Lindheim Red Hopster', matched['name'])

    def test_barrels(self):
        beer_list = [
            {'name': u'Nøgne Ø Imperial Stout (Whisky barrel edition)'}
        ]
        matcher = BeerNameMatcher(u'Nøgne Ø (Hansa Borg)', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Nøgne Ø Imperial Stout Whisky Barrels')
        self.assertEqual(u'Nøgne Ø Imperial Stout (Whisky barrel edition)', matched['name'])

    def test_amber_brewery(self):
        beer_list = [
            {'name': u'Amber Złote Lwy'}
        ]
        matcher = BeerNameMatcher(u'Browar Amber', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Zlote LWY Lys')
        self.assertEqual(u'Amber Złote Lwy', matched['name'])

    def test_mack_gull(self):
        beer_list = [
            {'name': u'Mack Gull'}
        ]
        matcher = BeerNameMatcher(u'Mack Bryggeri', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'GullMack')
        self.assertEqual(u'Mack Gull', matched['name'])

    def test_vuur_vlam(self):
        beer_list = [
            {'name': u'De Molen Vuur & Vlam (Fire & Flames)'}
        ]
        matcher = BeerNameMatcher(u'Brouwerij de Molen', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Brouwerij de Molen Vuur Vlam')
        self.assertEqual(u'De Molen Vuur & Vlam (Fire & Flames)', matched['name'])

    def test_faxe_premium(self):
        beer_list = [
            {'name': u'Royal Unibrew - Faxe Amber'},
            {'name': u'Faxe Extra Strong Danish Lager Beer'},
            {'name': u'Faxe Premium'}
        ]
        matcher = BeerNameMatcher(u'Royal Unibrew', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Faxe Premium Danish Lager Beer')
        self.assertEqual(u'Faxe Premium', matched['name'])

    def test_lindheim_saison(self):
        beer_list = [
            {'name': u'Lindheim Saison Farmhouse Ale Barrel Aged'},
            {'name': u'Lindheim Saison Farmhouse Ale'}
        ]
        matcher = BeerNameMatcher(u'Lindheim Ølkompani', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Lindheim Farmhouse Ale Saison')
        self.assertEqual(u'Lindheim Saison Farmhouse Ale', matched['name'])

    def test_mikkeller_barrel(self):
        beer_list = [
            {'name': u'Mikkeller Black Ink And Blood'},
            {'name': u'Mikkeller Black Ink And Blood Barrel Aged (Brandy Edition)'}
        ]
        matcher = BeerNameMatcher(u'Mikkeller', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Mikkeller Black Ink and Blood Imperial raspberry stout Brandy')
        self.assertEqual(u'Mikkeller Black Ink And Blood Barrel Aged (Brandy Edition)', matched['name'])

    def test_ola_dubh(self):
        beer_list = [
            {'name': u'Harviestoun - Harviestoun Ola Dubh 1991'},
            {'name': u'Harviestoun Ola Dubh (16 Year Old)'}
        ]
        matcher = BeerNameMatcher(u'Harviestoun', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Harviestoun Ola Dubh 16 special reserve ale')
        self.assertEqual(u'Harviestoun Ola Dubh (16 Year Old)', matched['name'])

    def test_kingfisher(self):
        beer_list = [
            {'name': u'Kingfisher Ultra Max'},
            {'name': u'Kingfisher (Premium) Lager Beer'}
        ]
        matcher = BeerNameMatcher(u'United Breweries Group', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Kingfisher Premium Lager')
        self.assertEqual(u'Kingfisher (Premium) Lager Beer', matched['name'])

    def test_retired(self):
        beer_list = [
            {'name': u'Flying Dog Snake Dog IPA (through 2007)', 'retired': True},
            {'name': u'Flying Dog Snake Dog IPA (2008 and later)'}
        ]
        matcher = BeerNameMatcher(u'Flying Dog Brewery', beer_list, abv_over=4.7, skip_retired=True)
        matched = matcher.match_name(u'Flying Dog Snake Dog IPA')
        self.assertEqual(u'Flying Dog Snake Dog IPA (2008 and later)', matched['name'])

    def test_samuel_smith(self):
        beer_list = [
            {'name': u'Samuel Smiths Taddy Porter'}
        ]
        matcher = BeerNameMatcher(u'Samuel Smith', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Samuel Smith Famous Taddy Porter')
        self.assertEqual(u'Samuel Smiths Taddy Porter', matched['name'])

    def test_soy_rodriguez(self):
        beer_list = [
            {'name': u'Edge Brewing Soy Rodríguez', 'abv': 5.3}
        ]
        matcher = BeerNameMatcher(u'Edge Brewing Barcelona', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Edge Soy Rodriguez Rye IPA')
        self.assertEqual(u'Edge Brewing Soy Rodríguez', matched['name'])

    def test_batch_500(self):
        beer_list = [
            {'name': u'Nøgne Ø # 500 Imperial India Pale Ale (Batch 500)'}
        ]
        matcher = BeerNameMatcher(u'Nøgne Ø (Hansa Borg)', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Nøgne Ø Imperial India Pale Ale #500')
        self.assertEqual(u'Nøgne Ø # 500 Imperial India Pale Ale (Batch 500)', matched['name'])

    def test_trappist_bier(self):
        beer_list = [
            {'name': u'La Trappe Bockbier'},
            {'name': u'La Trappe Tripel'}
        ]
        matcher = BeerNameMatcher(u'De Koningshoeven (Bavaria - Netherlands)', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'La Trappe Tripel Trappist Bier')
        self.assertEqual(u'La Trappe Tripel', matched['name'])

    def test_weissbier_hell(self):
        beer_list = [
            {'name': u'König Ludwig Hell'},
            {'name': u'König Ludwig Weissbier'}
        ]
        matcher = BeerNameMatcher(u'Schloßbrauerei Kaltenberg (Warsteiner)', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'König Ludwig Weissbier Hell')
        self.assertEqual(u'König Ludwig Weissbier', matched['name'])

    def test_oude_geuze(self):
        beer_list = [
            {'name': u'Chapeau Gueuze'},
            {'name': u'De Troch Oude Gueuze'}
        ]
        matcher = BeerNameMatcher(u'Brouwerij De Troch', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'De Troch Chapeau Oude Gueuze')
        self.assertEqual(u'De Troch Oude Gueuze', matched['name'])

    def test_crafty_dan(self):
        beer_list = [
            {'name': u'Thwaites Crafty Dan'},
            {'name': u'Thwaites Crafty Dan Triple C (Bottle, 5.3%)'}
        ]
        matcher = BeerNameMatcher(u'Thwaites', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Crafty Dan Triple C Golden Ale')
        self.assertEqual(u'Thwaites Crafty Dan Triple C (Bottle, 5.3%)', matched['name'])

    def test_gentse(self):
        beer_list = [
            {'name': u'Gruut Blond'},
            {'name': u'Gruut Belgian Wit Bier'}
        ]
        matcher = BeerNameMatcher(u'Gentse Stadsbrouwerij', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Gentse Gruut Wit')
        self.assertEqual(u'Gruut Belgian Wit Bier', matched['name'])

    def test_bottle_refermented(self):
        beer_list = [
            {'name': u'Green’s Tripel Blonde Ale'},
            {'name': u'Green’s Blond'}
        ]
        matcher = BeerNameMatcher(u'Green’s', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Green?s Bottle Refermented Blonde Ale')
        self.assertEqual(u'Green’s Blond', matched['name'])

    def test_hop_it(self):
        beer_list = [
            {'name': u'Urthel Hop-it'}
        ]
        matcher = BeerNameMatcher(u'Microbrouwerij Urthel', beer_list, abv_over=4.7)
        matched = matcher.match_name(u'Urthel Hop-It Superior Hoppig Blond')
        self.assertEqual(u'Urthel Hop-it', matched['name'])


    #def test_triple_collab(self):


    #Nøgne Ø Det kompromissløse Bry - Nøgne Ø # 100 :: Nøgne Ø (Hansa Borg) - Nøgne Ø # 1001


    #CAP Brewery - Cap/BrewDog CapDog Black IPA :: CAP Brewery - BrewDog / CAP CAP DOG
    #Nøgne Ø Det kompromissløse Bry - Nøgne Ø M.O.L.E. Russian Imperial Stout :: Nøgne Ø (Hansa Borg) - Nøgne Ø / La Chingoneria / Central Cervecera M.O.L.E.
    #Nøgne Ø Det kompromissløse Bry - Nøgne Ø India Saison :: Nøgne Ø (Hansa Borg) - Nøgne Ø / Bridge Road India Saison
    #Austmann Bryggeri - Austmann Caelum Caeruleum :: Austmann Bryggeri - Austmann / Balder / Lindheim Caelum Caeruelum

    #Amundsen/Grünerløkka Bryggeri - Amundsen/Grünerløkka Oslo IPA :: Amundsen Bryggeri & Spiseri - Amundsen Oslo Ølfestivaløl 2013
    #Amundsen/Grünerløkka Bryggeri - Amundsen/Grünerløkka Oslo IPA :: Grünerløkka Brygghus - Grünerløkka / Amundsen Oslo IPA