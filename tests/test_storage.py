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

    # add / in

    def test_empty_string(self):
        self.assertNotIn('', self.ct)
        self.ct.add('')
        self.assertIn('', self.ct)

    def test_one_word_in(self):
        w = "foo"
        self.ct.add(w)
        self.assertIn(w, self.ct)

    def test_two_words_empty_common_prefix(self):
        w1, w2 = "foo", "bar"
        self.ct.add(w1, w2)
        self.assertIn(w1, self.ct)
        self.assertIn(w2, self.ct)

    def test_two_words_with_common_prefix(self):
        w1, w2 = "fooqux", "foobar"
        self.ct.add(w1, w2)
        self.assertIn(w1, self.ct)
        self.assertIn(w2, self.ct)

    def test_two_words_with_one_prefix_of_the_other_first(self):
        w1, w2 = "foo", "foobar"
        self.ct.add(w1, w2)
        self.assertIn(w1, self.ct)
        self.assertIn(w2, self.ct)

    def test_two_words_with_one_prefix_of_the_other_second(self):
        w1, w2 = "foobar", "foo"
        self.ct.add(w1, w2)
        self.assertIn(w1, self.ct)
        self.assertIn(w2, self.ct)


    # remove

    def test_add_remove_one_word(self):
        w = "foowq"
        self.ct.add(w)
        self.assertIn(w, self.ct)
        self.ct.remove(w)
        self.assertNotIn(w, self.ct)
        self.assertTrue(self.ct.is_empty())

