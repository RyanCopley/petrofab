# -*- coding: utf-8 -*-
# native
import os

# fabric.api
from fabric.api import settings
from fabric.colors import green, red
from fabric.context_managers import cd
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
        self.env = teamocil
        self.name = name or self.env.get('name', None)
        self.filename = filename or self.env.get('filename', None)
        self.root = root or self.env.get('root', None)

    def _get_name(self, name):
        _name = name or self.name
        _name = _name or prompt(u'Teamocil layout name:')
        return _name

    def _get_filename(self, filename):
        _filename = filename or self.filename
        _filename = _filename or prompt(u'Teamocil layout filename:')
        return _filename

    def _get_root(self, root):
        _root = root or self.root
        _root = _root or prompt(u'Path to Teamocil root directory:')
        return path_abs(_root)

    def _get_layout(self, path, filename):
        layout = os.path.join(path, filename)
        if not os.path.isfile(layout):
            abort(red(u'"%s" not exists!' % layout))
        return layout

    def init_layout(self, name=None, filename=None):
        """Replace examples patterns in specific teamocil config."""
        self.name = self._get_name(name)
        self.filename = self._get_filename(filename)
        layout = self._get_layout(self.path, self.filename)
        repls = (
            (u'<example>', self.name),
            (u'<Example>', self.name.title()),
            (u'<example/path>', self.path),
        )
        with cd(self.path), settings(warn_only=True):
            for repl in repls:
                result = run('sed -i.bak -e \'s|{0}|{1}|g\' {file}'.format(
                    *repl, file=layout))
                if result.failed:
                    abort(red(result))
        print(green(u'Teamocil layout in "{0}" was init.').format(layout))

    def enable_layout(self, name=None, root=None, filename=None):
        """Make Teamocil layout in root directory."""
        self.name = self._get_name(name)
        self.root = self._get_root(root)
        self.filename = self._get_filename(filename)
        link = os.path.join(self.root, '%s.yml' % self.name)
        layout = self._get_layout(self.path, self.filename)
        with settings(warn_only=True):
            result = run('ln -s {0} {1}'.format(layout, link))
            if result.failed:
                abort(red(result))
        print(green(u'Teamocil layout "{.name}" enabled.').format(self))

    def disable_layout(self, name=None, root=None):
        self.name = self._get_name(name)
        self.root = self._get_root(root)
        link = os.path.join(self.root, '%s.yml' % self.name)
        with settings(warn_only=True):
            result = run('rm -f {0}'.format(link))
            if result.failed:
                abort(red(result))
        print(green(u'Teamocil layout "{.name}" disabled.').format(self))
