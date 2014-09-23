# -*- coding: utf-8 -*-
# fabric.api
from fabric.api import env
from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import run

# in-module
from .utils import get_config, path_abs

__all__ = [
    'subl_init_project',
]

# Update 'env' from default config
env.update(get_config())


@task
def subl_init_project(name, path=env.project['root']):
    """ Set name of Sublime Text project root file to current project name.

    Args:
        name (str): Name of new project.
        path (str): Path to new project, defaults to '~/work'.
    """
    path = path_abs(path)
    with cd(path):
        run('mv example.sublime-project {0}.sublime-project'.format(name))
