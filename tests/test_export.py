# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

import ctrie
from ctrie import CTrie

class TestExport(unittest.TestCase):
    pass
