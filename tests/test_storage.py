# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

import ctrie
from ctrie import CTrie

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.ct = CTrie()

    def test_empty(self):
        self.assertTrue(self.ct.is_empty())

    def test_empty_string(self):
        self.assertNotIn('', self.ct)
        self.ct.add('')
        self.assertIn('', self.ct)

    def test_one_word_in(self):
        w = "foo"
        self.ct.add(w)
        self.assertIn(w, self.ct)

