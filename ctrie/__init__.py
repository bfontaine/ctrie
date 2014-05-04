# -*- coding: UTF-8 -*-

"""
.. moduleauthor:: Baptiste Fontaine <b@ptistefontaine.fr>
"""

__version__ = '0.0.1'


def _isprefix(prefix, word):
    return word.startswith(prefix)

def _sliceprefix(prefix, word):
    return word[len(prefix):]

class CTrie(object):

    def __init__(self, terminal=False):
        self._children = {}
        self.terminal = terminal


    def _add(self, word):
        if word == '':
            if not self.terminal:
                self.terminal = True
                return True
            return False

        # one children with a prefix
        for prefix, child in self._children.items():
            if _isprefix(prefix, word):
                return child.add(_sliceprefix(prefix, word))

        # no children
        if not self._children:
            self._children[word] = CTrie(terminal=True)
            return True

        # TODO

        raise NotImplementedError


    # Remove a word from the trie, return True or False depending on if the
    # word was in the trie or not.
    def _remove(self, word):
        if word == '':
            self.terminal = False
            return True

        for prefix, child in self._children.items():
            if _isprefix(prefix, word):
                ret = child._remove(_sliceprefix(prefix, word))
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
            if _isprefix(prefix, word) and _sliceprefix(prefix, word) in child:
                return True

        return False
