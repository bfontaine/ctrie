# -*- coding: UTF-8 -*-

"""
This module provides a compact trie (``CTrie``) implementation for Python.

.. moduleauthor:: Baptiste Fontaine <b@ptistefontaine.fr>
"""

__version__ = '0.0.1'


def _is_prefix(prefix, word):
    return word.startswith(prefix)


def _slice_prefix(prefix, word):
    return word[len(prefix):]


# longuest common prefix
def _lcp(word1, word2):
    for i, (c1, c2) in enumerate(zip(word1, word2)):
        if c1 != c2:
            return word1[:i]

    return word1 if len(word1) < len(word2) else word2


class CTrie(object):
    """
    A compact trie. A trie, or prefix tree, is a data structure to efficiently
    store a set of strings with a lot of shared prefixes, like URLs.

    Compact tries are recursively defined, a trie has zero or more other
    child tries. A trie is said to be terminal if it contains the empty string.
    Each child is labelled with a prefix for its own children. For example, one
    compact trie that contains words "foo", "bar" and "foo42" has two children,
    one labelled "foo" and the other labelled "bar". The last one is terminal
    because once we read "bar" we can end our walk in the trie. The first one
    is terminal for the same reason, but have one terminal child labelled "42".
    In the following symbolic representation, a terminated child is represented
    with a dot at the end of its label: ::

         <empty>
            |
            +-- bar.
            |
            +-- foo.
                 |
                 +-- 42.

    Each possible walk in the trie, starting from the root and ending on a
    terminal node is a contained word. In the previous example, the empty
    string is not present in the trie because the root node is not terminal.

    A non-compact trie contains only one char per node.

    >>> from ctrie import CTrie
    >>> ct = CTrie()
    >>> c.add("foo", "bar", "qux")
    >>> "foo" in c
    True
    >>> "Bar" in c
    False
    >>> c.remove("foo")
    >>> "foo" in c
    False

    Keyword arguments:
            - ``terminal`` (``bool``, default: ``False``): specifies if the
              trie contains the empty string. This is the same as:

              >>> ct = CTrie()
              >>> ct.add('')  # empty string
    """

    def __init__(self, terminal=False):
        self._children = {}
        self.terminal = terminal

    def _add(self, word):
        # empty string
        if word == '':
            if not self.terminal:
                self.terminal = True
                return True
            return False

        # no child
        if not self._children:
            self._children[word] = CTrie(terminal=True)
            return True

        # one child with a common prefix
        for prefix, child in self._children.items():
            # one child with the word as a prefix
            if prefix == word:
                if not child.terminal:
                    child.terminal = True
                    return True
                return False

            if _is_prefix(prefix, word):
                return child.add(_slice_prefix(prefix, word))

        # split a child prefix
        for prefix, child in self._children.items():
            lcp = _lcp(prefix, word)
            if lcp:
                middle = CTrie()
                origin = _slice_prefix(lcp, prefix)
                new_branch = _slice_prefix(lcp, word)
                middle._children[origin] = child
                middle._children[new_branch] = CTrie(terminal=True)
                del self._children[prefix]
                self._children[lcp] = middle
                return True

        self._children[word] = CTrie(terminal=True)
        return True

    def _remove(self, word):
        """
        Remove a word from the trie.
        """
        if word == '':
            self.terminal = False
            return True

        for prefix, child in self._children.items():
            if _is_prefix(prefix, word):
                ret = child._remove(_slice_prefix(prefix, word))
                if child.is_empty():
                    del self._children[prefix]
                return ret

        return False

    def add(self, *words):
        """
        Add one or more words in the trie. The function returns ``True`` if all
        words were successfully added. It'll return ``False`` if one or more
        words were already present in the trie.
        """
        ret = True
        for word in words:
            ret &= self._add(word)

        return ret

    def remove(self, *words):
        """
        Remove one or more words from the trie. The function returns ``True``
        if all the words were successfully removed (i.e. they were in the trie
        before) or ``False`` if one or more words couldn't be found in the
        trie.
        """
        ret = True
        for word in words:
            ret &= self._remove(word)

        return ret

    def is_empty(self):
        """
        Return ``True`` if the trie is empty.
        """
        return not (self._children or self.terminal)

    def __contains__(self, word):
        if word == '' and self.terminal:
            return True

        for prefix, child in self._children.items():
            if _is_prefix(prefix, word) and \
                    _slice_prefix(prefix, word) in child:
                return True

        return False
