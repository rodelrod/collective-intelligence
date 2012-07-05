#!/usr/bin/env python
import unittest
import deliciousrec as drec
from mock import Mock
from delicious_posts_mock import POSTS


class MockDelicious(object):
    """Mimics the delicious API:  

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

    def test_initialize_userdict(self):
        mock_pydlc = MockDelicious()
        drec.pydlc.get_popular = mock_pydlc.get_popular
        drec.pydlc.get_urlposts = mock_pydlc.get_urlposts
        expected = {
            'fulano': {},
            'sicrano': {},
            'beltrano': {},
            'escher': {},
            'bach': {},
            'bartok': {}}
        actual = drec.initialize_userdict('programming')
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
