# -*- coding: utf-8 -*-
# native
import os

# fabric.api
from fabric.api import env, settings
from fabric.colors import green, red, yellow
from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import prompt, run
from fabric.utils import abort

# fabric.contrib
from fabric.contrib.console import confirm

# in-module
from .utils import get_config, path_abs

__all__ = [
    'proj_clean',
    'proj_create_dirs',
    'proj_src_clone',
    'proj_tmpl_clone',
]

# Update 'env' from default config
env.update(get_config())


@task
def proj_create_dirs(name, path=env.project['root']):
    """Create dirs structure for new project.

    Create project's dirs in base catalog:
    <some path>/
        <name>/
            src/
            tmp/

    Returns:
        Path to new project.
    """
    path = os.path.join(path, name)
    path = path_abs(path, False)
    with settings(warn_only=True):
        if run('mkdir -p %s' % path).failed:
            abort(red(u'Can\'t create directory!'))
    print(green(u'Project directories structure was created!'))
    return path


@task
def proj_tmpl_clone(path=env.project['root']):
    """Clone template of project.

    Clone template of project from GitHub:
    https://github.com/petrikoz/project-template

    Args:
        path (str): Path to new project, defaults to '~/work'.
    """
    path = path_abs(path)
    tmpl_url = env.project['tmpl']
    with settings(warn_only=True):
        if run('git clone {0} {1}'.format(tmpl_url, path)).failed:
            abort(red(u'Can\'t clone template of project!'))
    print(green(u'Project template was clone.'))


@task
def proj_clean(path=env.project['root'], silently=False):
    """Remove trash from cloned tmpl.

    Args:
        path (str): Path to new project, defaults to '~/work'.
        silently (bool): signal for ask user about confirm operation.
    """
    msg = yellow(u'Be careful! This operation will not cancel! Continue?')
    if not silently and not confirm(msg):
        abort(red(u'Canceled by user!'))
    path = path_abs(path)
    with cd(path):
        run('find . -iname ".gitkeep" -print0 | xargs -0 rm -rf')
        run('find . -iname "readme.*" -print0 | xargs -0 rm -rf')
        run('rm -rf .git')
    print(green(u'Project directories is clean now.'))


@task
def proj_src_clone(repo=env.project['src'], path=env.project['root']):
    """Clone source code of project.

    Args:
        repo (str): URL of repo with source code, defaults is None.
        path (str): Path to new project, defaults to '~/work'.
    """
    path = path_abs(path)
    path = os.path.join(path, 'src')
    if repo is None:
        repo = prompt('Enter URL of repo with source code:')
    with settings(warn_only=True):
        if run('git clone {0} {1}'.format(repo, path)).failed:
            abort(red(u'Can\'t clone source code!'))
    print(green(u'Source code successfully cloned.'))
