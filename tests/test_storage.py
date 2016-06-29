# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

from ctrie import CTrie

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.ct = CTrie()

    # empty

    def test_empty(self):
        self.assertTrue(self.ct.is_empty())

    def test_terminal_not_empty(self):
        ct = CTrie(terminal=True)
        self.assertFalse(ct.is_empty())
        self.ct.add('')
        self.assertFalse(self.ct.is_empty())

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


    # values

    def test_empty_values(self):
        self.assertSequenceEqual([], list(self.ct.values()))

    def test_value_empty_string(self):
        self.ct.add('')
        self.assertSequenceEqual([''], list(self.ct.values()))

    def test_one_level_values(self):
        strs = ['foo', 'bar', 'qux']
        self.ct.add(*strs)
        self.assertSequenceEqual(sorted(strs), sorted(list(self.ct.values())))

    def test_large_trie_values(self):
        strs = ['foo', 'bar', 'qux', 'faa', 'foobar', 'qax', 'zoo', 'qwerty',
                'azerty', 'hello', 'hi', 'home', 'barfoo', 'barfoobar', 'z',
                'f', 'b', 'fd', 'fdd', 'word', 'words', 'wood', 'woo']
        self.ct.add(*strs)
        self.assertSequenceEqual(sorted(strs), sorted(list(self.ct.values())))

    # subtree

    def test_empty_subtree_empty_prefix(self):
        st = self.ct.subtree('')
        self.assertSequenceEqual([], list(st.values()))

    def test_empty_subtree(self):
        st = self.ct.subtree('something')
        self.assertSequenceEqual([], list(st.values()))

    def test_subtree_empty_prefix(self):
        strs = ['foo', 'foobar']
        self.ct.add(*strs)
        st = self.ct.subtree('')
        self.assertSequenceEqual(sorted(strs), sorted(st.values()))

    def test_subtree_nonmatching_prefix(self):
        self.ct.add('a', 'b', 'c', 'd')
        st = self.ct.subtree('e')
        self.assertSequenceEqual([], list(st.values()))

    def test_subtree_matching_prefix(self):
        self.ct.add('fooa', 'foob', 'fooc', 'food')
        st = self.ct.subtree('foo')
        self.assertSequenceEqual(['a', 'b', 'c', 'd'], sorted(st.values()))

    def test_subtree_matching_prefix_cut(self):
        self.ct.add('fooa', 'foob', 'fooc', 'food')
        st = self.ct.subtree('fo')
        self.assertSequenceEqual(['oa', 'ob', 'oc', 'od'], sorted(st.values()))

    # ==

    def test_eq_empty_other_collections(self):
        self.assertFalse(self.ct == [])
        self.assertFalse(self.ct == ())
        self.assertFalse(self.ct == set())

    def test_eq_empty_tries(self):
        self.assertTrue(CTrie() == CTrie())

    def test_eq_terminal(self):
        c2 = CTrie()
        c2.add('')
        self.assertFalse(self.ct == c2)
        self.assertFalse(c2 == self.ct)

        self.ct.add('')
        self.assertTrue(self.ct == c2)
        self.assertTrue(c2 == self.ct)

    def test_not_eq(self):
        c2 = CTrie()
        c2.add('a', 'b', 'c', 'aa', 'ab', 'ac')
        self.assertFalse(self.ct == c2)
        self.assertFalse(c2 == self.ct)

        self.ct.add('a', 'c', 'ab', 'ac')
        self.assertFalse(self.ct == c2)
        self.assertFalse(c2 == self.ct)

        self.ct.add('b', 'ab')
        self.ct.remove('a')
        self.assertFalse(self.ct == c2)
        self.assertFalse(c2 == self.ct)

    def test_eq(self):
        strs = ['a', 'ab', 'abc', 'abd', 'ba', 'x', 'zz', 'zx']
        c2 = CTrie()
        c2.add(*strs)
        self.ct.add(*strs)

        self.assertTrue(c2 == self.ct)
        self.assertTrue(self.ct == c2)

    def test_eq_different_internal_structure(self):
        c2 = CTrie()
        c2.add('abcdef', 'abcxyz')
        c2.remove('abcxyz')

        self.ct.add('abcdef')
        self.assertTrue(c2 == self.ct)
        self.assertTrue(self.ct == c2)

    # iter

    def test_iter(self):
        strs = ['foo', 'bar', 'qux', 'baar', 'fo', 'fooo']
        self.ct.add(*strs)
        self.assertSequenceEqual(sorted(strs), sorted(e for e in self.ct))

    # iadd

    def test_iadd(self):
        self.ct += ['foo', 'bar']
        self.assertIn('foo', self.ct)
        self.assertIn('bar', self.ct)
