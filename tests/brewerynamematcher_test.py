# -*- coding: utf-8 -*-

import unittest

from brewerynamematcher import match_name

BREWERIES = [
    {"name": "Brasserie de l’Abbaye des Rocs", "id": 1},
    {"name": "Brasserie de l’Abbaye du Val-Dieu", "id": 2},
    {"name": "Brasserie de la Croix - Sainte Nitouche ", "id": 3},
    {"name": "Brasserie de la Gleize", "id": 4},
    {"name": "Ringnes Bryggeri (Carlsberg)", "id": 5},
    {"name": "Aass", "id": 6},

]


class BreweryNameMatcherTest(unittest.TestCase):

    def test_match_similar_name(self):
        matched = match_name('Aass', BREWERIES)
        self.assertEqual(6, matched['id'])

    def test_match_name_with_different_case(self):
        matched = match_name('aass', BREWERIES)
        self.assertEqual(6, matched['id'])

    def test_match_name_with_different_case2(self):
        matched = match_name('AASS', BREWERIES)
        self.assertEqual(6, matched['id'])

    def test_match_name_with_abbreviation(self):
        pass

    def test_match_name_with_corporation(self):
        matched = match_name('Ringnes Bryggeri', BREWERIES)
        self.assertEqual(5, matched['id'])

    def test_match_name_with_common_stuff(self):
        matched = match_name('Aass Bryggeri', BREWERIES)
        self.assertEqual(6, matched['id'])

    def test_match_name_with_case_coop_and_common(self):
        matched = match_name('ringnes', BREWERIES)
        self.assertEqual(5, matched['id'])

    def test_match_difficult_name(self):
        matched = match_name('Abbaye des Rocs', BREWERIES)
        self.assertEqual(1, matched['id'])

    def test_match_brasserie(self):
        matched = match_name('Gleize', BREWERIES)
        self.assertEqual(4, matched['id'])