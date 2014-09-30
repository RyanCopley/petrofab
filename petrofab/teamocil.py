# -*- coding: utf-8 -*-
# native
import fileinput
import os

# fabric.api
from fabric.api import settings
from fabric.colors import green, red
from fabric.operations import prompt, run
from fabric.utils import abort

# in-module
from .utils import path_abs

__all__ = [
    'Teamocil',
]


class Teamocil(object):

    """Class for work with Teamocil.

    See https://github.com/remiprev/teamocil.
    """

    def __init__(self, path, name=None, filename=None, root=None, teamocil={}):
        super(Teamocil, self).__init__()
        self.path = path_abs(path)
        self.name = name
        self.filename = filename or teamocil.get('filename', '')
        self.env = teamocil
        self.root = root

    def init_layout(self, name=None):
        """Replace examples patterns in specific teamocil config."""

        _path = self.path
        _name = name or self.name or self.env.get('name', None)
        _name = _name or prompt(u'Teamocil layout name:')
        self.name = _name
        layout = os.path.join(_path, self.filename)
        if not os.path.isfile(layout):
            abort(red(u'"%s" not exists!' % layout))
        for line in fileinput.input(layout, inplace=True):
            new = line.rstrip()
            new = new.replace(u'<example>', _name)
            new = new.replace(u'<Example>', _name.title())
            new = new.replace(u'<example/path>', _path)
            print(new)
        print(green(u'Teamocil layout in "{0}" was init.').format(layout))

    def make_layout(self, root=None, name=None):
        """Make Teamocil layout in root directory."""
        _path = self.path
        _root = root or self.root or self.env.get('root', None)
        _root = _root or prompt(u'Path to Teamocil root directory:')
        self.root = path_abs(_root)
        _name = name or self.name or self.env.get('name', None)
        _name = _name or prompt(u'Teamocil layout name:')
        self.name = _name
        link = os.path.join(self.root, '%s.yml' % _name)
        layout = os.path.join(_path, self.filename)
        if not os.path.isfile(layout):
            abort(red(u'"%s" not exists!' % layout))
        with settings(warn_only=True):
            result = run('ln -s {0} {1}'.format(layout, link))
            if result.failed:
                abort(red(result))
        print(green(u'Teamocil layout "{0}" was create.').format(_name))
