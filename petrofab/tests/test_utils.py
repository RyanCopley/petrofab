# -*- coding: utf-8 -*-
# native
import json
import os
import sys
import unittest
from StringIO import StringIO

# in-project
import petrofab
from ..utils import get_config, path_abs


class PathAbsTest(unittest.TestCase):
    """Test suit for 'petrofab.utils.path_abs' function."""

    def setUp(self):
        self.standard_path = os.path.dirname(
            os.path.dirname(os.path.abspath(petrofab.__file__))
        )
        # Capture sys.stderr
        self.held_stderr, sys.stderr = sys.stderr, StringIO()

    def tearDown(self):
        sys.stderr = self.held_stderr

    def test_path_is_absolute(self):
        """Path must be absolute."""
        first = os.path.join(self.standard_path, 'tmp')
        second = path_abs('./tmp', check=False)
        self.assertEqual(first, second)

    def test_path_not_exists(self):
        """Check path exists by default."""
        with self.assertRaises(SystemExit):
            path_abs('./tmp')
        path = os.path.join(self.standard_path, 'tmp')
        msg = u'Path "{0}" not exists!'.format(path)
        sys_msg = sys.stderr.getvalue().strip()
        self.assertIn(msg, sys_msg)


class GetConfigTest(unittest.TestCase):
    """Test suit for 'petrofab.utils.path_abs' function."""

    def setUp(self):
        self.config_dict = {
            'hosts': '...',
            'project': '...',
            'teamocil': '...'
        }
        # Config in 'tmp' folder
        self.config_file = '/tmp/.petrofab.json'
        json.dump(self.config_dict, open(self.config_file, 'w+'))
        # Tmp dir for test 'is_file'
        self.config_dir = '/tmp/.petrofab'
        os.makedirs(self.config_dir)
        # Config for check defaults pathes
        self.config_default = '.petrofab.json'
        json.dump(self.config_dict, open(self.config_default, 'w+'))
        # Capture sys.stderr
        self.held_stderr, sys.stderr = sys.stderr, StringIO()

        # Custom Fabric 'env'
        class Fabenv(object):
            pass
        self.fabenv = Fabenv()

    def tearDown(self):
        if os.path.isfile(self.config_file):
            os.remove(self.config_file)
        if os.path.isdir(self.config_dir):
            os.removedirs(self.config_dir)
        if os.path.isfile(self.config_default):
            os.remove(self.config_default)
        sys.stderr = self.held_stderr

    def test_config_path_is_file(self):
        """Config must be file."""
        with self.assertRaises(SystemExit):
            get_config(self.fabenv, self.config_dir)
        msg = u'Config "{0}" not exists!'.format(self.config_dir)
        sys_msg = sys.stderr.getvalue().strip()
        self.assertIn(msg, sys_msg)

    def test_config_update_env(self):
        """Result must has attrs from config"""
        _env = get_config(self.fabenv, self.config_file)
        for attr in self.config_dict.keys():
            self.assertTrue(hasattr(_env, attr))

    def test_config_defaults(self):
        """Check default configs."""
        _env = get_config(self.fabenv)
        for attr in self.config_dict.keys():
            self.assertTrue(hasattr(_env, attr))
