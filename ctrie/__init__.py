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

    def add(self, word):
        if word == '':
            self.terminal = True
            return

        for prefix, child in self._children.items():
            if _isprefix(prefix, word):
                return child.add(_sliceprefix(prefix, word))

        if not self._children:
            self._children[word] = CTrie(terminal=True)
            return

        # TODO

        raise NotImplementedError

    def remove(self, word):
        if word == '' and self.terminal:
            self.terminal = False
            return

        raise NotImplementedError

    def __contains__(self, word):
        if word == '' and self.terminal:
            return True

        for prefix, child in self._children.items():
            if _isprefix(prefix, word) and _sliceprefix(prefix, word) in child:
                return True

        return False
