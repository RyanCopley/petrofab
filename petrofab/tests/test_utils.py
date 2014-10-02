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


class UtilsTest(unittest.TestCase):

    def setUp(self):
        self.config_dict = {
            "hosts": ["localhost"],
            "project": {
                "path": ".",
                "url": "https://github.com/petrikoz/project-template.git"
            },
            "teamocil": {
                "root": "~/.teamocil",
                "filename": ".teamocil.yml"
            }
        }
        self.config_file = '/tmp/.petrofab.json'
        self.standard_path = os.path.dirname(
            os.path.dirname(os.path.abspath(petrofab.__file__))
        )
        # Capture sys.stderr
        self.held_stderr, sys.stderr = sys.stderr, StringIO()

        # Custom Fabric 'env'
        class Fabenv(object):
            pass
        self.fabenv = Fabenv()

    def tearDown(self):
        if os.path.isfile(self.config_file):
            os.remove(self.config_file)
        if os.path.isdir(self.config_file):
            os.removedirs(self.config_file)
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

    def test_config_path_is_dir(self):
        """Path to config must be directory."""
        msg = u'"{0}" must be directory!'
        with open(self.config_file, 'w') as config:
            path = os.path.abspath(config.name)
            with self.assertRaises(SystemExit):
                get_config(self.fabenv, path)
            msg = msg.format(path)
        sys_msg = sys.stderr.getvalue().strip()
        self.assertIn(msg, sys_msg)

    def test_config_path_is_file(self):
        """Config must be file."""
        if os.path.exists(self.config_file):
            raise AssertionError
        os.makedirs(self.config_file)
        with self.assertRaises(SystemExit):
            get_config(self.fabenv, '/tmp')
        os.removedirs(self.config_file)
        msg = u'File "{0}" not exists!'.format(self.config_file)
        sys_msg = sys.stderr.getvalue().strip()
        self.assertIn(msg, sys_msg)

    def test_config_update_env(self):
        """Result must has attrs from config"""
        json.dump(self.config_dict, open(self.config_file, 'w+'))
        _env = get_config(self.fabenv, '/tmp')
        for attr in self.config_dict.keys():
            self.assertTrue(hasattr(_env, attr))
