#!/usr/bin/env python
"""Test file for deliciousrec.py"""
import unittest
import deliciousrec as drec
from delicious_posts_mock import POSTS


class MockDelicious(object):

    """Mocks a subset of the pydelicious API for testing.

    We assume a single tag per post for simplification.

    """

    def __init__(self, posts=POSTS):
        self.posts = posts
         
    def get_popular(self, tag):
        return [post for post in self.posts if post['tags'] == tag]

    def get_userposts(self, user):
        return [post for post in self.posts if post['user'] == user]

    def get_urlposts(self, url):
        return [post for post in self.posts if post['url'] == url]


class TestDeliciousRec(unittest.TestCase):

    def setUp(self):
        mock_pydlc = MockDelicious()
        drec.pydlc.get_popular = mock_pydlc.get_popular
        drec.pydlc.get_urlposts = mock_pydlc.get_urlposts
        drec.pydlc.get_userposts = mock_pydlc.get_userposts

    def test_initialize_userdict(self):
        expected = {
                'fulano': {},
                'sicrano': {},
                'beltrano': {},
                'escher': {},
                'bach': {},
                'bartok': {}}
        actual = drec.initialize_userdict('programming')
        self.assertEqual(actual, expected)

    def test_fill_items(self):
        user_dict = {
                'fulano': {},
                'sicrano': {},
                'beltrano': {},
                'escher': {},
                'bach': {},
                'bartok': {}}
        expected = {
                'fulano': {
                    'theonlinephotographer.com': 1.0,
                    'joelonsoftware.com': 1.0,
                    'django.org': 1.0,
                    'codecomplete.com': 1.0,
                    'news.ycombinator.com': 1.0,
                    'python.org': 1.0,
                    'publico.pt': 0.0,
                    'nyt.com': 0.0,
                    'dn.pt': 0.0},
                'sicrano': {
                    'codecomplete.com': 1.0,
                    'django.org': 1.0,
                    'dn.pt': 0.0,
                    'joelonsoftware.com': 1.0,
                    'news.ycombinator.com': 1.0,
                    'nyt.com': 1.0,
                    'publico.pt': 1.0,
                    'python.org': 1.0,
                    'theonlinephotographer.com': 1.0},
                'beltrano': {
                    'codecomplete.com': 1.0,
                    'django.org': 0.0,
                    'dn.pt': 1.0,
                    'joelonsoftware.com': 1.0,
                    'news.ycombinator.com': 1.0,
                    'nyt.com': 1.0,
                    'publico.pt': 1.0,
                    'python.org': 1.0,
                    'theonlinephotographer.com': 0.0},
                'escher': {
                    'codecomplete.com': 0.0,
                    'django.org': 0.0,
                    'dn.pt': 0.0,
                    'joelonsoftware.com': 0.0,
                    'news.ycombinator.com': 1.0,
                    'nyt.com': 1.0,
                    'publico.pt': 1.0,
                    'python.org': 0.0,
                    'theonlinephotographer.com': 0.0},
                'bach': {
                    'codecomplete.com': 0.0,
                    'django.org': 0.0,
                    'dn.pt': 0.0,
                    'joelonsoftware.com': 1.0,
                    'news.ycombinator.com': 1.0,
                    'nyt.com': 0.0,
                    'publico.pt': 0.0,
                    'python.org': 0.0,
                    'theonlinephotographer.com': 0.0},
                'bartok': {
                    'codecomplete.com': 1.0,
                    'django.org': 0.0,
                    'dn.pt': 0.0,
                    'joelonsoftware.com': 1.0,
                    'news.ycombinator.com': 1.0,
                    'nyt.com': 1.0,
                    'publico.pt': 0.0,
                    'python.org': 0.0,
                    'theonlinephotographer.com': 1.0}}
        actual = drec.fill_items(user_dict)
        self.assertEqual(actual, expected)

    def test_recommend_links(self):
        """Apply recommendation engine to the delicious data set"""
        pass

if __name__ == '__main__':
    unittest.main()
