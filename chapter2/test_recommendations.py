#!/usr/bin/env python
import unittest
from recommendations import *

class TestRecommendations(unittest.TestCase):

    def round_sequence(self, seq, nb_digits=5):
        """Inspects a nested sequence and rounds the floats to nb_digits"""
        def round_float(x):
            if isinstance(x, float):
                return round(x, nb_digits)
            elif isinstance(x, list) or isinstance(x, tuple):
                return self.round_sequence(x, nb_digits)
            else:
                return x
        rounded =  map(round_float, seq)
        if isinstance(seq, tuple):
            rounded = tuple(rounded)
        return rounded

    def test_round_sequence(self):
        actual = self.round_sequence(
                [(1.23456, 'a'), (2.34567, 'b'), (3.45678, 'c')], 2)
        expected = [(1.23, 'a'), (2.35, 'b'), (3.46, 'c')]
        self.assertEqual(actual, expected)

    def setUp(self):
        self.prefs = {'fulano': {'coco': 2.1, 'ranheta': 1.1}, 
                      'sicrano': {'facada':4.5},
                      'beltrano': {'coco':3.2, 'ranheta': 1.2, 'facada': 3.4}}

    def test_sim_distance(self):
        distance = sim_distance(self.prefs, 'fulano', 'beltrano')
        self.assertAlmostEqual(distance, 0.47516409872148213)

    def test_sim_distance_no_common_films(self):
        distance = sim_distance(self.prefs, 'fulano', 'sicrano')
        self.assertEqual(distance, 0)

    def test_get_shared_movies(self):
        self.assertEqual(get_shared_movies(self.prefs, 'fulano', 'sicrano'), 
                    [])
        self.assertEqual(get_shared_movies(self.prefs, 'fulano', 'beltrano'), 
                    ['coco', 'ranheta'])
        self.assertEqual(get_shared_movies(self.prefs, 'sicrano', 'beltrano'), 
                    ['facada'])

    def test_get_rating_across_movie_list(self):
        ratings = get_rating_across_movie_list(self.prefs, 'fulano', ['coco'])
        self.assertEqual(ratings, [2.1])

    def test_average(self):
        self.assertEqual(average([2,3,3,8]), 4)

    def test_stdev(self):
        self.assertAlmostEqual(stdev([2,3,3,5,6,8]), 2.0615528128088303)
        self.assertAlmostEqual(stdev2([2,3,3,5,6,8]), 2.0615528128088303)

    def test_stdev2(self):
        self.assertAlmostEqual(stdev([2,3,3,5,6,8]), 2.0615528128088303)
        self.assertAlmostEqual(stdev2([2,3,3,5,6,8]), 2.0615528128088303)

    def test_cov(self):
        self.assertAlmostEqual(
                cov([2,3,3,5,6,8,8,8,4,1,1,2], [5,4,3,7,3,5,5,4,5,2,2,3]),
                1.8333333333333333)

    def test_pearson_corr(self):
         self.assertAlmostEqual(
                pearson_corr([2,3,3,5,6,8,8,8,4,1,1,2], [5,4,3,7,3,5,5,4,5,2,2,3]),
                0.501296346484753)

    def test_sim_pearson(self):
        distance = sim_pearson(self.prefs, 'fulano', 'beltrano')
        self.assertAlmostEqual(distance, 1.)
        book_distance = sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
        self.assertAlmostEqual(book_distance, 0.396059017191)

    def test_topMatches(self):
        actual = topMatches(critics,'Toby',n=3)
        expected = [(0.99124070716192991, 'Lisa Rose'), 
                    (0.92447345164190486, 'Mick LaSalle'), 
                    (0.89340514744156474, 'Claudia Puig')]
        self.assertIsInstance(actual, list)
        self.assertEqual(
                self.round_sequence(actual), 
                self.round_sequence(expected))

    def test_getRecommendations(self):
        actual = getRecommendations(critics,'Toby')
        expected = [(3.3477895267131013, 'The Night Listener'), 
                    (2.8325499182641614, 'Lady in the Water'), 
                    (2.5309807037655645, 'Just My Luck')]
        self.assertIsInstance(actual, list)
        self.assertEqual(
                self.round_sequence(actual), 
                self.round_sequence(expected))

if __name__ == '__main__':
    unittest.main()
