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

    def test_add_empty_string(self):
        self.assertNotIn('', self.ct)
        self.assertTrue(self.ct.add(''))
        self.assertIn('', self.ct)

    def test_add_nothing(self):
        self.assertTrue(self.ct.add())

    def test_add_one_word_in(self):
        w = "foo"
        self.assertTrue(self.ct.add(w))
        self.assertIn(w, self.ct)

    def test_add_duplicates(self):
        w = "foo"
        self.assertTrue(self.ct.add(w))
        self.assertFalse(self.ct.add(w))
        self.assertIn(w, self.ct)

    def test_add_duplicate_empty(self):
        self.assertTrue(self.ct.add(''))
        self.assertFalse(self.ct.add(''))
        self.assertIn('', self.ct)

    def test_two_words_empty_common_prefix(self):
        w1, w2 = "foo", "bar"
        self.assertTrue(self.ct.add(w1, w2))
        self.assertIn(w1, self.ct)
        self.assertIn(w2, self.ct)

    def test_two_words_with_common_prefix(self):
        w1, w2 = "fooqux", "foobar"
        self.assertTrue(self.ct.add(w1, w2))
        self.assertIn(w1, self.ct)
        self.assertIn(w2, self.ct)

    def test_two_words_with_one_prefix_of_the_other_first(self):
        w1, w2 = "foo", "foobar"
        self.assertTrue(self.ct.add(w1, w2))
        self.assertIn(w1, self.ct)
        self.assertIn(w2, self.ct)

    def test_two_words_with_one_prefix_of_the_other_second(self):
        w1, w2 = "foobar", "foo"
        self.assertTrue(self.ct.add(w1, w2))
        self.assertIn(w1, self.ct)
        self.assertIn(w2, self.ct)

    def test_two_words_with_one_prefix_of_the_other_after_split(self):
        w1, w2, w3 = "foobar", "fooqux", "foo"
        self.assertTrue(self.ct.add(w1, w2, w3))
        self.assertIn(w1, self.ct)
        self.assertIn(w2, self.ct)
        self.assertIn(w3, self.ct)

    def test_dupe_two_words_with_one_prefix_of_the_other_after_split(self):
        w1, w2, w3, w4 = "foobar", "fooqux", "foo", "foo"
        self.assertTrue(self.ct.add(w1, w2, w3))
        self.assertFalse(self.ct.add(w4))
        self.assertIn(w1, self.ct)
        self.assertIn(w2, self.ct)
        self.assertIn(w3, self.ct)


    # remove

    def test_add_remove_one_word(self):
        w = "foowq"
        self.assertTrue(self.ct.add(w))
        self.assertIn(w, self.ct)
        self.assertTrue(self.ct.remove(w))
        self.assertNotIn(w, self.ct)
        self.assertTrue(self.ct.is_empty())

    def test_add_remove_nothing(self):
        w = "foowq"
        self.assertTrue(self.ct.add(w))
        self.assertTrue(self.ct.remove())

    def test_remove_unfound_word(self):
        self.assertFalse(self.ct.remove("something"))

    def test_add_remove_multiple_word(self):
        w1, w2, w3 = "foowq", "fooqw", "bar"
        self.assertTrue(self.ct.add(w1, w2, w3))
        self.assertTrue(self.ct.remove(w1, w2, w3))
        self.assertNotIn(w1, self.ct)
        self.assertNotIn(w2, self.ct)
        self.assertNotIn(w3, self.ct)


    # len

    def test_empty_len(self):
        self.assertEqual(0, len(self.ct))

    def test_one_word_len(self):
        self.ct.add('foo')
        self.assertEqual(1, len(self.ct))

    def test_one_word_prefix_of_another_len(self):
        self.ct.add('foo', 'foobar')
        self.assertEqual(2, len(self.ct))

    def test_multiple_words_len(self):
        words = ['foo', 'q', 'bar', 's o m e t h i n g', 'hello']
        self.ct.add(*words)
        self.assertEqual(len(words), len(self.ct))


    # height

    def test_empty_height(self):
        self.assertEqual(0, self.ct.height())

    def test_one_level_height(self):
        self.ct.add('foo', 'bar', 'qux')
        self.assertEqual(1, self.ct.height())

    def test_two_level_height(self):
        self.ct.add('foo', 'fbar', 'qux')
        self.assertEqual(2, self.ct.height())

    def test_large_trie_height(self):
        self.ct.add('aaa', 'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb')
        self.assertEqual(3, self.ct.height())
