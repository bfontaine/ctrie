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

    def test_is_in(self):
        w = "foo"
        self.ct.add(w)
        self.assertIn(w, self.ct)

