# -*- coding: utf-8 -*-
# native
import unittest

# in-project
from ..sublime import Sublime


class SublimeTest(unittest.TestCase):

    def test_insufficient_args(self):
        """Check constructor of 'Sublime' class."""
        # Must take 2 params
        self.assertRaises(TypeError, Sublime, 'foo')

        # Path must exists
        self.assertRaises(SystemExit, Sublime, 'foo', '/foo')
