#!/usr/bin/env python
from __future__ import division
import unittest
import recommendations as rec
import math

def floor_n(x, n):
    return math.floor(x*(10**n)) / 10**n

def trunc_n(x, n):
    return math.trunc(x*(10**n)) / 10**n

def round_sequence(seq, nb_digits=5, roundf=round):
    """Inspects a nested sequence and rounds the floats to ``nb_digits``
    
    Alternate functions can be given to replace the round method. 
    They must respect the signature f(x, n)

    """
    def round_float(x):
        if isinstance(x, float):
            return roundf(x, nb_digits)
        elif isinstance(x, list) or isinstance(x, tuple):
            return round_sequence(x, nb_digits, roundf)
        else:
            return x
    rounded =  map(round_float, seq)
    if isinstance(seq, tuple):
        rounded = tuple(rounded)
    return rounded


class TestRoundSequence(unittest.TestCase):

    def test_round_sequence(self):
        actual = round_sequence(
                [(1.23456, 'a'), (2.34567, 'b'), (-3.45678, 'c')], 2)
        expected = [(1.23, 'a'), (2.35, 'b'), (-3.46, 'c')]
        self.assertEqual(actual, expected)

    def test_round_sequence_floor(self):
        actual = round_sequence(
                [(1.23456, 'a'), (2.34567, 'b'), (-3.45678, 'c')], 
                nb_digits=2, roundf=floor_n)
        expected = [(1.23, 'a'), (2.34, 'b'), (-3.46, 'c')]
        self.assertEqual(actual, expected)

    def test_round_sequence_trunc(self):
        actual = round_sequence(
                [(1.23456, 'a'), (2.34567, 'b'), (-3.45678, 'c')], 
                nb_digits=2, roundf=trunc_n)
        expected = [(1.23, 'a'), (2.34, 'b'), (-3.45, 'c')]
        self.assertEqual(actual, expected)


class TestRecommendations(unittest.TestCase):

    def setUp(self):
        self.prefs = {'fulano': {'coco': 2.1, 'ranheta': 1.1}, 
                      'sicrano': {'facada':4.5},
                      'beltrano': {'coco':3.2, 'ranheta': 1.2, 'facada': 3.4}}

    def test_sim_distance(self):
        distance = rec.sim_distance(self.prefs, 'fulano', 'beltrano')
        self.assertAlmostEqual(distance, 0.47516409872148213)

    def test_sim_distance_no_common_films(self):
        distance = rec.sim_distance(self.prefs, 'fulano', 'sicrano')
        self.assertEqual(distance, 0)

    def test_get_shared_movies(self):
        self.assertEqual(
                rec.get_shared_movies(self.prefs, 'fulano', 'sicrano'), 
                [])
        self.assertEqual(
                rec.get_shared_movies(self.prefs, 'fulano', 'beltrano'), 
                ['coco', 'ranheta'])
        self.assertEqual(
                rec.get_shared_movies(self.prefs, 'sicrano', 'beltrano'), 
                ['facada'])

    def test_get_rating_across_movie_list(self):
        ratings = rec.get_rating_across_movie_list(self.prefs, 'fulano', ['coco'])
        self.assertEqual(ratings, [2.1])

    def test_average(self):
        self.assertEqual(rec.average([2,3,3,8]), 4)

    def test_stdev(self):
        self.assertAlmostEqual(rec.stdev([2,3,3,5,6,8]), 2.0615528128088303)
        self.assertAlmostEqual(rec.stdev2([2,3,3,5,6,8]), 2.0615528128088303)

    def test_stdev2(self):
        self.assertAlmostEqual(rec.stdev([2,3,3,5,6,8]), 2.0615528128088303)
        self.assertAlmostEqual(rec.stdev2([2,3,3,5,6,8]), 2.0615528128088303)

    def test_cov(self):
        self.assertAlmostEqual(
                rec.cov([2,3,3,5,6,8,8,8,4,1,1,2], [5,4,3,7,3,5,5,4,5,2,2,3]),
                1.8333333333333333)

    def test_pearson_corr(self):
        self.assertAlmostEqual(
                rec.pearson_corr([2,3,3,5,6,8,8,8,4,1,1,2], [5,4,3,7,3,5,5,4,5,2,2,3]),
                0.501296346484753)

    def test_sim_pearson(self):
        distance = rec.sim_pearson(self.prefs, 'fulano', 'beltrano')
        self.assertAlmostEqual(distance, 1.)
        book_distance = rec.sim_pearson(rec.critics, 'Lisa Rose', 'Gene Seymour')
        self.assertAlmostEqual(book_distance, 0.396059017191)

    def test_topMatches(self):
        actual = rec.topMatches(rec.critics,'Toby',n=3)
        expected = [(0.99124070716192991, 'Lisa Rose'), 
                    (0.92447345164190486, 'Mick LaSalle'), 
                    (0.89340514744156474, 'Claudia Puig')]
        self.assertIsInstance(actual, list)
        self.assertEqual(
                round_sequence(actual), 
                round_sequence(expected))

    def test_getRecommendations(self):
        actual = rec.getRecommendations(rec.critics,'Toby')
        expected = [(3.3477895267131013, 'The Night Listener'), 
                    (2.8325499182641614, 'Lady in the Water'), 
                    (2.5309807037655645, 'Just My Luck')]
        self.assertIsInstance(actual, list)
        self.assertEqual(
                round_sequence(actual), 
                round_sequence(expected))

    def test_transformPrefs(self):
        byname = {'Lisa Rose': 
                      {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5},
                  'Gene Seymour': 
                      {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5}}
        bymovie = {'Lady in the Water':
                      {'Lisa Rose':2.5,'Gene Seymour':3.0},
                   'Snakes on a Plane':
                      {'Lisa Rose':3.5,'Gene Seymour':3.5}} 
        actual = rec.transformPrefs(byname)
        expected = bymovie
        self.assertEqual(actual, expected)

    def test_topMatches_movies(self):
        movies = rec.transformPrefs(rec.critics)
        matches_long = rec.topMatches(movies, 'Superman Returns')
        matches = round_sequence(matches_long, 3, trunc_n) 
        self.assertEqual(
                matches,
                [(0.657, 'You, Me and Dupree'), 
                 (0.487, 'Lady in the Water'), 
                 (0.111, 'Snakes on a Plane'), 
                 (-0.179, 'The Night Listener'), 
                 (-0.422, 'Just My Luck')])


if __name__ == '__main__':
    unittest.main()
