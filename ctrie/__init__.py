# -*- coding: UTF-8 -*-

"""
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


# A compact trie
class CTrie(object):

    # Create a trie
    def __init__(self, terminal=False):
        self._children = {}
        self.terminal = terminal

    # Add one word to the trie
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

    # Remove a word from the trie, return True or False depending on if the
    # word was in the trie or not. This function might result in an unoptimized
    # trie.
    def _remove(self, word):
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

    # Add one or more words in the trie. The function returns True if all words
    # were successfully added. It'll return False if one or more words were
    # already present in the trie.
    def add(self, *words):
        ret = True
        for word in words:
            ret &= self._add(word)

        return ret

    # Remove one or more words from the trie. The function returns True if all
    # the words were successfully removed (i.e. they were in the trie before)
    # or False if one or more words couldn't be found in the trie.
    def remove(self, *words):
        ret = True
        for word in words:
            ret &= self._remove(word)

        return ret

    # Check if the trie is empty
    def is_empty(self):
        return not (self._children or self.terminal)

    def __contains__(self, word):
        if word == '' and self.terminal:
            return True

        for prefix, child in self._children.items():
            if _is_prefix(prefix, word) and \
                    _slice_prefix(prefix, word) in child:
                return True

        return False
