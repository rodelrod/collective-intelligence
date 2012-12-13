#!/usr/bin/env python
# vi:fileencoding=utf-8
import unittest
import generatefeedvector as gfv
from mock import Mock, patch
import pickle

class TestGenerateFeedVector(unittest.TestCase):

    def setUp(self):
        gfv.getfeed = Mock(return_value=pickle.load(open('feed.p', 'rb')))

    def test_strip_hml(self):
        self.assertEqual(gfv.strip_html('<p>test</p>'), 'test')
        self.assertEqual(
                gfv.strip_html("<html><body bgcolor='cyan'>test </body></html>"), 
                'test ')
 
    def test_getwordcounts(self):
        title, wc = gfv.getwordcounts('fake_url')
        self.assertEqual(title, u'Schneier on Security')
        self.assertEqual(wc[u'security'], 6)
        self.assertEqual(wc[u'forensic'], 3)
        self.assertRaises(KeyError, wc.__getitem__, u'[...]')
        self.assertRaises(KeyError, wc.__getitem__, u'')

    def test_main(self):
        pass

if __name__ == '__main__':
    unittest.main()
