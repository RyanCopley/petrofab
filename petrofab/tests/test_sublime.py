# -*- coding: utf-8 -*-
# native
import sys
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# in-project
from .. import sublime
from ..sublime import subl_project


class SublimeTest(unittest.TestCase):

    def setUp(self):
        self.proj_name = 'foo'
        self.proj_path = '/tmp'
        self.env = {'baz': 'bar'}
        self.rename = sublime.rename
        # Capture sys.stderr
        self.held_stderr, sys.stderr = sys.stderr, StringIO()

    def tearDown(self):
        sys.stderr = self.held_stderr
        sublime.rename = self.rename

    def _test_construct_params(self):
        self.assertTrue(hasattr(subl_project, 'proj_name'))
        self.assertEqual(subl_project.proj_name, self.proj_name)
        self.assertTrue(hasattr(subl_project, 'proj_path'))
        self.assertEqual(subl_project.proj_path, self.proj_path)
        self.assertTrue(hasattr(subl_project, 'env'))
        self.assertEqual(subl_project.env.keys(), self.env.keys())
        self.assertEqual(subl_project.env.values(), self.env.values())

    def test_insufficient_args(self):
        """Check constructor of 'Sublime' class."""
        # Monkey patch rename for checking args
        sublime.rename = lambda n, p: 'Rename'
        subl_project.run(name=self.proj_name, path=self.proj_path,
                         config=self.env)
        self._test_construct_params()

        # Monkey patch user input
        sublime.prompt = lambda _: self.proj_name
        subl_project.run(path=self.proj_path, config=self.env)
        self._test_construct_params()

    def test_rename_path_exists(self):
        """Path must exist which sended in function 'rename'."""
        path = '/foo'
        with self.assertRaises(SystemExit):
            self.rename(self.proj_name, path)
        msg = 'Path "{0}" not exists!'.format(path)
        sys_msg = sys.stderr.getvalue().strip()
        self.assertIn(msg, sys_msg)
