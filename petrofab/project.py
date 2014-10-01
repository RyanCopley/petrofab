# -*- coding: utf-8 -*-
# native
import os

# fabric.api
from fabric.api import settings
from fabric.colors import green, red, yellow
from fabric.context_managers import cd
from fabric.operations import prompt, run
from fabric.utils import abort

# fabric.contrib
from fabric.contrib.console import confirm

# in-module
from .utils import path_abs

__all__ = [
    'Project',
]


class Project(object):
    """Class for create project."""
    def __init__(self, name, path, project={}, url=None, src=None, trash=[]):
        super(Project, self).__init__()
        self.name = name
        self.path = path_abs(path)
        self.env = project
        self.url = url or self.env.get('url', None)
        self.src = src or self.env.get('src', None)
        self.trash = trash or self.env.get('trash', ['.git*', 'readme.*'])

    def make_path(self):
        """Create root path of project."""
        _path = os.path.join(self.path, self.name)
        self.path = _path
        with settings(warn_only=True):
            result = run('mkdir -p %s' % _path)
            if result.failed:
                abort(red(result))
        print(green(u'"{path}" was create.').format(**self.__dict__))

    def get_template(self, url=None):
        """Clone template of project dirs.

        Clone template of project from GitHub:
        https://github.com/petrikoz/project-template

        Args:
            url (str): URL to repo with project template.
        """
        _url = url or self.url
        self.url = _url or prompt(u'URL to repo with template:')
        with settings(warn_only=True):
            result = run('git clone {0} {1}'.format(self.url, self.path))
            if result.failed:
                msg = result
                abort(red(msg.format(**self.__dict__)))
        print(green(u'"{url}" was clone.').format(**self.__dict__))

    def clean(self, trash=[], silently=False):
        """Remove trash from cloned tmpl.

        Args:
            trash (list): list of patterns which will remove.
            silently (bool): signal for ask user about confirm operation.
        """
        self.trash = trash or self.trash
        msg = yellow(u'Be careful! This operation will not cancel! Continue?')
        if not silently and not confirm(msg):
            print(red(u'Canceled by user!'))
            return
        with cd(self.path):
            for pattern in self.trash:
                run('find . -iname "%s" -print0 | xargs -0 rm -rf' % pattern)
        print(green(u'"{path}" was clean.').format(**self.__dict__))

    def get_source_code(self, src=None):
        """Clone source code of project.

        Args:
            src (str): URL of repo with source code, defaults is None.
            path (str): Path to new project, defaults to '~/work'.
        """
        _path = os.path.join(self.path, 'src')
        _src = src or self.src
        self.src = _src or prompt(u'Enter URL of repo with source code:')
        with settings(warn_only=True):
            result = run('git clone {0} {1}'.format(self.src, _path))
            if result.failed:
                abort(red(result))
        print(green(u'"{src}" was clone.').format(**self.__dict__))
