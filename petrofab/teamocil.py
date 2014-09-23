# -*- coding: utf-8 -*-
# native
import fileinput
import os

# fabric.api
from fabric.api import env
from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import run

# in-module
from .utils import get_config, path_abs

__all__ = [
    'teamocil_init_layout',
]

# Update 'env' from default config
env.update(get_config())


@task
def teamocil_init_layout(name, path=env.project['root']):
    """Create Teamocil item for new project.

    See https://github.com/remiprev/teamocil.

    Replace example patterns in project's file '.teamocil.yml'.
    After create symbol link of this file in '~/.teamocil/'.

    Args:
        name (str): Name of new project.
        path (str): Path to new project, defaults to '~/work'.
    """
    path = path_abs(path)
    with cd(path):
        teamocil_proj = os.path.join(path, env.teamocil['filename'])
        for line in fileinput.input(teamocil_proj, inplace=True):
            new = line.rstrip()
            new = new.replace(u'<example>', name)
            new = new.replace(u'<Example>', name.title())
            new = new.replace(u'<example/path>', path)
            print(new)
        teamocil_item = os.path.join(env.teamocil['root'],
                                     '{0}.yml'.format(name))
        run('ln -s {0} {1}'.format(teamocil_proj, teamocil_item))
