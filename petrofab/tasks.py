# -*- coding: utf-8 -*-
# native
import sys

# fabric.api
from fabric.api import env
from fabric.colors import cyan
from fabric.decorators import task
from fabric.operations import prompt

# fabric.contrib
from fabric.contrib.console import confirm

# in-module
from .project import (
    proj_clean, proj_create_dirs, proj_src_clone, proj_tmpl_clone
)
from .sublime import subl_init_project
from .teamocil import teamocil_init_layout
from .utils import get_config

__all__ = [
    'mk_proj',
]

# Update 'env' from default config
env.update(get_config())


@task
def mk_proj(name=None, path=env.project['root']):
    """Create new project.

    Args:
        name (unicode): Name of new project, defaults to None.
        path (str): Path to new project, defaults to '~/work'.
    """
    project = {
        'name': name or prompt(u'Project name:'),
        'path': path,
    }
    project['path'] = proj_create_dirs(**project)
    proj_tmpl_clone(project['path'])
    proj_clean(project['path'], silently=True)
    subl_init_project(**project)
    # Teamocil
    if confirm(u'Init Teamocil?', default=False):
        teamocil_init_layout(**project)
    # Src
    if confirm(u'Clone source code of project?', default=False):
        proj_src_clone(path=project['path'])
    msg = (u'Project was created:\n'
           u'\tName:\t{name}\n'
           u'\tPath:\t{path}')
    msg = msg.format(name=project['name'],
                     path=project['path'].decode(sys.stdin.encoding))
    msg = msg.encode(sys.stdout.encoding)
    print(cyan(msg))
