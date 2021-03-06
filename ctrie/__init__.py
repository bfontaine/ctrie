# -*- coding: UTF-8 -*-

"""
This module provides a compact trie (``CTrie``) implementation for Python.

.. moduleauthor:: Baptiste Fontaine <b@ptistefontaine.fr>
"""

__version__ = '0.1.1'

from io import StringIO


def _cut_prefix(prefix, word):
    """
    test if ``prefix`` is a prefix of ``word``. If so, return the trailing part
    of ``word``, or ``None`` if not.
    """
    if word.startswith(prefix):
        return word[len(prefix):]


def _longuest_common_prefix(word1, word2):
    for i in range(min(len(word1), len(word2))):
        if word1[i] != word2[i]:
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
    >>> len(c)
    2

    Keyword arguments:
            - ``terminal`` (``bool``, default: ``False``): specifies if the
              trie contains the empty string. This is the same as:

              >>> ct = CTrie()
              >>> ct.add('')  # empty string
    """

    __slots__ = ['_children', 'terminal']

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

            trailing = _cut_prefix(prefix, word)
            if trailing is not None:
                return child.add(trailing)

        # split a child prefix
        """
        The goal of the code below is to (if possible) go from the following
        trie:

            <root>
              |
              ...
              +-- foobar
                    |
                    +-- qux

        to the following one, after insertion of the word 'foo123':

            <root>
              |
              ...
              +-- foo
                    |
                    +-- bar
                    |    |
                    |    +-- qux
                    |
                    +-- 123

        We're essentially creating an intermediate node (called ``middle`` in
        the following code) with the good prefix, which is the longest common
        prefix between the original node prefix and the inserted word.
        """
        for prefix, child in self._children.items():
            lcp = _longuest_common_prefix(prefix, word)
            if lcp:
                middle = CTrie()
                origin = prefix[len(lcp):]
                new_branch = word[len(lcp):]
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
            trailing = _cut_prefix(prefix, word)
            if trailing is not None:
                ret = child._remove(trailing)
                if child.is_empty():
                    del self._children[prefix]
                return ret

        return False

    def add(self, *words):
        """
        Add one or more words in the trie. The function returns ``True`` if all
        words were successfully added. It'll return ``False`` if one or more
        words were already present in the trie.

        >>> ct = CTrie()
        >>> ct.add('foo', 'bar')
        True
        >>> 'foo' in ct
        True
        >>> ct.add('bar')
        False
        >>> ct.add('qux')
        True
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

        >>> ct = CTrie()
        >>> ct.add('foo', 'qux')
        True
        >>> 'foo' in ct
        True
        >>> ct.remove('foo', 'bar')
        False
        >>> 'foo' in ct
        False
        >>> ct.remove('qux')
        >>> True
        """
        ret = True
        for word in words:
            ret &= self._remove(word)

        return ret

    def is_empty(self):
        """
        Return ``True`` if the trie is empty.

        >>> ct = CTrie()
        >>> ct.is_empty()
        True
        >>> ct.add('')
        True
        >>> ct.is_empty()
        False
        """
        return not (self._children or self.terminal)

    def height(self):
        """
        Compute the height of the trie. An empty trie has a zero height, and
        the maximum height of a compacted trie is the length of its longuest
        word.

        >>> ct = CTrie()
        >>> ct.height()
        0
        >>> ct.add(''); ct.height()
        0
        >>> ct.add('foo'); ct.height()
        1
        >>> ct.add('bar'); ct.height()
        1
        >>> ct.add('boo'); ct.height()
        2

        .. versionadded:: 0.1.0
        """
        if not self._children:
            return 0

        return 1 + max(map(lambda c: c.height(), self._children.values()))

    def values(self):
        """
        Yield all values from this trie in arbitrary order. The order in which
        they're yielded doesn't depend on the order in which they're inserted.

        >>> ct = CTrie()
        >>> ct.add('foo', 'bar', 'qux')
        True
        >>> for x in ct.values(): print x
        ...
        qux
        foo
        bar

        .. versionadded:: 0.1.0
        """
        if self.is_empty():
            return

        if self.terminal:
            yield ''

        for prefix, child in self._children.items():
            for value in child.values():
                yield prefix + value

    def subtree(self, prefix):
        """
        Return a subtree that's equivalent to the current one with all values
        stripped from the given prefix. Values that don't start with this
        prefix are not included.
        An empty trie is returned if the prefix doesn't match any value.

        Note that the returned subtree may share its nodes with the current
        one.

        >>> ct = CTrie()
        >>> ct.add('foo', 'bar', 'foobar', 'fooo', 'qux')
        True
        >>> foo = ct.subtree('foo')
        >>> list(foo)  # actual order may vary
        ['', 'bar', 'o']
        >>> ct.subtree('nope').is_empty()
        True
        """
        if prefix == '':
            return self

        if prefix in self._children:
            return self._children[prefix]

        for node_prefix, node in self._children.items():
            lcp = _longuest_common_prefix(prefix, node_prefix)
            if not lcp:
                continue

            root = CTrie()
            child = CTrie()

            suffix = node_prefix[len(lcp):]

            root._children[suffix] = child
            child._children = node._children
            return root

        return CTrie()

    def _write_pretty_string(self, writer, indent_string):
        if self.terminal:
            writer.write("\n")

        for prefix, ch in self._children.items():
            writer.write("%s%s" % (indent_string, prefix))
            ch._write_pretty_string(writer, indent_string + " " * len(prefix))

        return writer

    def write_pretty_string(self, writer):
        """
        Equivalent of ``pretty_string`` that uses the given writer's ``.write``
        method.
        """
        return self._write_pretty_string(writer, "")

    def pretty_string(self):
        """
        Return a pretty-printed version of the internal state of the tree. It
        helps understand how words are split to fit in a tree.
        """
        writer = self.write_pretty_string(StringIO())
        writer.seek(0)
        return writer.read()

    # Export
    # ======

    def to_dict(self):
        """
        Recursively convert the tree to a dictionary.
        """
        return {
            "terminal": self.terminal,
            "children": {prefix: ch.to_dict()
                            for prefix, ch in self._children.items()},
        }

    @classmethod
    def from_dict(cls, d):
        """
        Take a dictionary in the format returned by ``to_dict`` and build a new
        instance.
        """
        instance = CTrie(terminal=bool(d.get("terminal")))

        children = d.get("children", {})
        if children:
            for prefix, ch in children.items():
                instance._children[prefix] = cls.from_dict(ch)

        return instance


    # Magic Methods
    # =============

    def __contains__(self, word):
        """
        Check if the trie contains a given word.
        """
        if word == '' and self.terminal:
            return True

        for prefix, child in self._children.items():
            trailing = _cut_prefix(prefix, word)
            if trailing is not None and trailing in child:
                return True

        return False

    def __len__(self):
        """
        Compute the number of words in the trie. This result should be cached
        because we're recursively checking every node in the trie.
        """
        total = 1 if self.terminal else 0
        for ch in self._children.values():
            total += len(ch)
        return total

    def __eq__(self, other):
        """
        Two compact tries are equal if they contain the same set of words. This
        doesn't guarantee the internal structures are equal.
        """
        if not isinstance(other, CTrie):
            return False

        # Bad complexity but there may be multiple compact tries that recognize
        # the same set of words because we don't re-compact a trie when we
        # remove a bunch of words from it.
        for word in self.values():
            if word not in other:
                return False

        for word in other.values():
            if word not in self:
                return False

        return True

    def __iter__(self):
        return self.values()

    def __nonzero__(self):
        return not self.empty()

    def __iadd__(self, other):
        for word in other:
            self._add(word)
        return self

    def __ior__(self, other):
        return self.__iadd__(other)

    def __isub__(self, other):
        for word in other:
            self._remove(word)
        return self

    def __iand__(self, other):
        words_to_remove = []

        for word in self.values():
            if word not in other:
                words_to_remove.append(word)

        for word in words_to_remove:
            self._remove(word)

        return self
