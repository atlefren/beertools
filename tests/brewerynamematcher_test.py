# -*- coding: utf-8 -*-

import unittest

from brewerynamematcher import BreweryNameMatcher

BREWERIES = [
    {"name": u"Brasserie de l’Abbaye des Rocs", "id": 1},
    {"name": u"Brasserie de l’Abbaye du Val-Dieu", "id": 2},
    {"name": u"Brasserie de la Croix - Sainte Nitouche ", "id": 3},
    {"name": u"Brasserie de la Gleize", "id": 4},
    {"name": u"Ringnes Bryggeri (Carlsberg)", "id": 5},
    {"name": u"Aass", "id": 6},
    {"name": u"Sierra Nevada Brewing Company", "id": 7},
    {"name": u"Brasserie Fantôme", "id": 8},
    {"name": u"Amundsen Bryggeri & Spiseri", "id": 9},
    {"name": u"Dugges Ale & Porterbryggeri", "id": 10},
    {"name": u"Brasserie dOrval", "id": 11},
    {"name": u"Brasserie St-Feuillien / Friart", "id": 12},
    {"name": u"Lervig Aktiebryggeri", "id": 13},
    {"name": u"The Dux Brewing Co.", "id": 14},
    {"name": u"Wild Beer", "id": 15},
    {"name": u"la Mule", "id": 16},
    {"name": u"Brasserie Artisanale de Rulles", "id": 17},
    {"name": u"Coisbo Beer", "id": 18},
    {"name": u"Coniston", "id": 19},
    {"name": u"Mondi Beer", "id": 20},
    {"name": u"Cervezas Moritz", "id": 21},
    {"name": u"Marbäcks öl", "id": 22},
    {"name": u"Mack Bryggeri", "id": 23},
    {"name": u"Irving", "id": 24},
    {"name": u"Kirin Brewery Company", "id": 25},
    {"name": u"De Leite", "id": 26},
    {"name": u"Trappistenbrouwerij De Kievit", "id": 27},
    {"name": u"Charles Wells", "id": 28},
    {"name": u"Parish", "id": 29},
    {"name": u"Vliegende Paard Brouwers", "id": 30},
    {"name": u"Privateer", "id": 31},
    {"name": u"Pivovar Náchod (LIF)", "id": 32},
    {"name": u"Orlando Brewing Company", "id": 33},
    {"name": u"Greene King", "id": 34},
    {"name": u"Hatebrew", "id": 35},
    {"name": u"Duggan’s Brewery", "id": 36},
    {"name": u"Selsinger Hofbräu", "id": 37},
    {"name": u"Cölner Hofbräu P. Josef Früh", "id": 38},
    {"name": u"Brewcrafts Microbrewing", "id": 39},
    {"name": u"Thwaites", "id": 40},
    {"name": u"Ecaussinnes", "id": 41},
    {"name": u"Clan!Destino?", "id": 42},
    {"name": u"Cerveza Artesanal Nomade", "id": 43},
    {"name": u"Cervecera Ceriux", "id": 44},
    {"name": u"Ruhrtal Brauerei", "id": 45},
    {"name": u"pendrups Bryggeri", "id": 46},
    {"name": u"Brauerei Dantscher", "id": 47},
    {"name": u"Brouwerij Malheur (formerly De Landtsheer)", "id": 48},
    {"name": u"BrauKunstKeller", "id": 49},
    {"name": u"Brasserie des Fagnes", "id": 50},
    {"name": u"Brauerei Landsberg", "id": 51},
    {"name": u"Rotburger", "id": 52},
    {"name": u"Bitburger Brauerei Th. Simon", "id": 53},
    {"name": u"Boring Brewing Company", "id": 54},
    {"name": u"Hansa Borg Bryggerier", "id": 55},
    {"name": u"Baikal Brewing Company  (Heineken)", "id": 56},
    {"name": u"Bavik-De Brabandere", "id": 57},
    {"name": u"Balmain Brewing Company", "id": 58},
    {"name": u"Le Baladin", "id": 59},
    {"name": u"Adnams", "id": 60},
    {"name": u"Aja Bryggeri", "id": 61},
    {"name": u"Budějovický Budvar", "id": 62},
    {"name": u"Brouwerij Omer Vander Ghinste", "id": 63},
    {"name": u"CRAK Brewery", "id": 64},
    {"name": u"Green’s", "id": 65},
    {"name": u"Damm", "id": 66},
    {"name": u"Fuller’s", "id": 67},
    {"name": u"De Proefbrouwerij", "id": 68},
    {"name": u"Královský pivovar Krušovice (Heineken)", "id": 69},
    {"name": u"Schloßbrauerei Kaltenberg (Warsteiner)", "id": 70},
    {"name": u"Tucher Bräu Fürth (Oetker Group)", "id": 71},
    {"name": u"Malmgårdin Panimo - Malmgard Brewery", "id": 72},
    {"name": u"Brauerei Gusswerk", "id": 73},
    {"name": u"Brewfist", "id": 74},
    {"name": u"OWA Brewery SPRL", "id": 75},
    {"name": u"Cerveceria Birrart", "id": 76},
    {"name": u"L’Esperluette", "id": 77},
    {"name": u"Boon Rawd Brewery", "id": 78},
    {"name": u"Stift Engelszell Trappistenbier-Brauerei", "id": 79},
    {"name": u"Sektkellerei Gebrüder Szigeti", "id": 80},
    {"name": u"Bardic Wells Meadery", "id": 81},
    {"name": u"Redhook Brewery", "id": 82},
    {"name": u"8th Street Ale Haus", "id": 83},
    {"name": u"#Freedom Craft Brewery", "id": 84},
    {"name": u"Kona Brewing Company", "id": 85},
]


class BreweryNameMatcherTest(unittest.TestCase):

    def setUp(self):
        self.matcher = BreweryNameMatcher(BREWERIES)

    def test_match_similar_name(self):
        matched = self.matcher.match_name('Aass')
        self.assertEqual(u'Aass', matched['name'])

    def test_match_name_with_different_case(self):
        matched = self.matcher.match_name('aass')
        self.assertEqual(u'Aass', matched['name'])

    def test_match_name_with_different_case2(self):
        matched = self.matcher.match_name('AASS')
        self.assertEqual(u'Aass', matched['name'])

    def test_match_name_with_corporation(self):
        matched = self.matcher.match_name('Ringnes Bryggeri')
        self.assertEqual(u'Ringnes Bryggeri (Carlsberg)', matched['name'])

    def test_match_name_with_common_stuff(self):
        matched = self.matcher.match_name('Aass Bryggeri')
        self.assertEqual(u'Aass', matched['name'])

    def test_match_name_with_common_stuff2(self):
        matched = self.matcher.match_name('Sierra Nevada Brewing Co.')
        self.assertEqual(u'Sierra Nevada Brewing Company', matched['name'])

    def test_match_name_with_case_coop_and_common(self):
        matched = self.matcher.match_name('ringnes')
        self.assertEqual(u'Ringnes Bryggeri (Carlsberg)', matched['name'])

    def test_match_difficult_name(self):
        matched = self.matcher.match_name('Abbaye des Rocs')
        self.assertEqual(u'Brasserie de l’Abbaye des Rocs', matched['name'])

    def test_match_brasserie(self):
        matched = self.matcher.match_name('Gleize')
        self.assertEqual(u'Brasserie de la Gleize', matched['name'])

    def test_match_accents(self):
        matched = self.matcher.match_name('Fantome')
        self.assertEqual(u'Brasserie Fantôme', matched['name'])

    def test_match_collab(self):
        matched = self.matcher.match_name(u'Amundsen/Grünerløkka Bryggeri')
        self.assertEqual(u'Amundsen Bryggeri & Spiseri', matched['name'])

    def test_match_misspelling(self):
        matched = self.matcher.match_name(u'Dugges Ale- & Porterbryggeri A')
        self.assertEqual(u'Dugges Ale & Porterbryggeri', matched['name'])

    def test_match_orval(self):
        matched = self.matcher.match_name(u'Brasserie d\'Orval')
        self.assertEqual(u'Brasserie dOrval', matched['name'])

    def test_match_feuillien(self):
        matched = self.matcher.match_name(u'Brasserie St. Feuillien')
        self.assertEqual(u'Brasserie St-Feuillien / Friart', matched['name'])

    def test_match_misspelling2(self):
        matched = self.matcher.match_name(u'Lervig Aktiebrygeri')
        self.assertEqual(u'Lervig Aktiebryggeri', matched['name'])

    def test_match_wild_beer(self):
        matched = self.matcher.match_name(u'The Wild Beer Co')
        self.assertEqual(u'Wild Beer', matched['name'])

    def test_match_rulles(self):
        matched = self.matcher.match_name(u'La Rulles')
        self.assertEqual(u'Brasserie Artisanale de Rulles', matched['name'])

    def test_match_coisbo(self):
        matched = self.matcher.match_name(u'Coisbo')
        self.assertEqual(u'Coisbo Beer', matched['name'])

    def test_match_moriz(self):
        matched = self.matcher.match_name(u'Moritz Beer')
        self.assertEqual(u'Cervezas Moritz', matched['name'])

    def test_match_mack(self):
        matched = self.matcher.match_name(u'Macks Ølbryggeri')
        self.assertEqual(u'Mack Bryggeri', matched['name'])

    def test_match_kirin(self):
        matched = self.matcher.match_name(u'Kirin')
        self.assertEqual(u'Kirin Brewery Company', matched['name'])

    def test_match_kievit(self):
        matched = self.matcher.match_name(u'De Kievit')
        self.assertEqual(u'Trappistenbrouwerij De Kievit', matched['name'])

    def test_match_baladin(self):
        matched = self.matcher.match_name(u'Baladin')
        self.assertEqual(u'Le Baladin', matched['name'])

   # @unittest.skip("gah")
    def test_match_bavik(self):
        matched = self.matcher.match_name(u'Bavik Brewery')
        self.assertEqual(u'Bavik-De Brabandere', matched['name'])

    def test_match_engelszell(self):
        matched = self.matcher.match_name(u'Stift Engelszell')
        self.assertEqual(u'Stift Engelszell Trappistenbier-Brauerei', matched['name'])

    @unittest.skip("gah")
    def test_match_crak(self):
        matched = self.matcher.match_name(u'CR/AK Brewery s.r.l.')
        self.assertEqual(u'CRAK Brewery', matched['name'])

    def test_match_owa(self):
        matched = self.matcher.match_name(u'Owa Brewery')
        self.assertEqual(u'OWA Brewery SPRL', matched['name'])

    def test_match_brewfist(self):
        matched = self.matcher.match_name(u'NiuBru S.R.L. - Brewfist')
        self.assertEqual(u'Brewfist', matched['name'])

    def test_match_bitburger(self):
        matched = self.matcher.match_name(u'Bitburger Brauerei')
        self.assertEqual(u'Bitburger Brauerei Th. Simon', matched['name'])

    def test_match_colner(self):
        matched = self.matcher.match_name(u'Cölner Hofbräu')
        self.assertEqual(u'Cölner Hofbräu P. Josef Früh', matched['name'])

    def test_match_adnams(self):
        matched = self.matcher.match_name(u'Adnams Sole Bay Brewery')
        self.assertEqual(u'Adnams', matched['name'])

    def test_match_szigeti(self):
        matched = self.matcher.match_name(u'Szigeti')
        self.assertEqual(u'Sektkellerei Gebrüder Szigeti', matched['name'])

    def test_match_dugges(self):
        matched = self.matcher.match_name(u'Dugges')
        self.assertEqual(u'Dugges Ale & Porterbryggeri', matched['name'])

    def test_match_blank(self):
        matched = self.matcher.match_name(u'')
        self.assertEqual(None, matched)

    def test_match_young_co(self):
        matched = self.matcher.match_name(u'Young & Co Brewery')
        self.assertEqual(None, matched)

    def test_match_redhook(self):
        matched = self.matcher.match_name(u'Redhook Ale Brewery')
        self.assertEqual(u'Redhook Brewery', matched['name'])

    def test_match_kona(self):
        matched = self.matcher.match_name(u'Kona Brewing Co.')
        self.assertEqual(u'Kona Brewing Company', matched['name'])
