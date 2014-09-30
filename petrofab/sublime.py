# -*- coding: utf-8 -*-
# fabric.api
from fabric.api import settings
from fabric.colors import green, red
from fabric.context_managers import cd
from fabric.operations import run
from fabric.utils import abort

# in-module
from .utils import path_abs

__all__ = [
    'Sublime',
]


class Sublime(object):

    """docstring for Sublime"""

    def __init__(self, name, path):
        super(Sublime, self).__init__()
        self.name = name
        self.path = path_abs(path)

    def make_project(self):
        """ Set name of Sublime project."""
        with cd(self.path), settings(warn_only=True):
            result = run(('mv example.sublime-project'
                          ' {0}.sublime-project').format(self.name))
            if result.failed:
                abort(red(result))
        print(green(u'Sublime project was init.'))
