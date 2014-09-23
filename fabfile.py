# -*- coding: utf-8 -*-
# native
import fileinput
import json
import os
import sys

# fabric.contrib
from fabric.contrib.console import confirm
from fabric.contrib.files import exists

# fabric.api
from fabric.api import env, settings
from fabric.colors import cyan, green, red, yellow
from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import prompt, run
from fabric.utils import abort

__root = os.path.dirname(os.path.abspath(__file__))

# Utils


def _get_config():
    conf_file_name = getattr(env, 'config_file', 'fab.conf')
    print(conf_file_name)
    json_data = open(os.path.join(__root, conf_file_name))
    config = json.load(json_data)
    return config


_MSG_SEPARATOR = u'-' * 32


def _show_msg(msg):
    """Show message.

    Args:
        msg (str): Message will shown.
    """
    print(_MSG_SEPARATOR + u'\n')
    print(msg)
    print(u'\n' + _MSG_SEPARATOR)


def _path_abs(path, check=True):
    """Return absolute path for some destination.

    Args:
        path (str): some path.
        check (bool): check path exists, default is True.

    Returns:
        String is containing absolute path of arg 'path'.
    """
    path = os.path.expanduser(path)
    path = os.path.normcase(path)
    path = os.path.normpath(path)
    path = os.path.abspath(path)
    if check and not exists(path):
        msg = u'Path "%s" not exists!' % path.decode(sys.stdin.encoding)
        msg = msg.encode(sys.stdout.encoding)
        abort(red(msg))
    return path


# Environment
env.update(_get_config())


# Project


@task
def proj_create_dirs(name, path=env.project['root']):
    """Create dirs structure for new project.

    Create project's dirs in base catalog:
    <some path>/
        <name>/
            project_files/
            tmp/

    Returns:
        Path to new project.
    """
    path = os.path.join(path, name)
    path = _path_abs(path, False)
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
    path = _path_abs(path)
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
    path = _path_abs(path)
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
    path = _path_abs(path)
    path = os.path.join(path, 'src')
    if repo is None:
        repo = prompt('Enter URL of repo with source code:')
    with settings(warn_only=True):
        if run('git clone {0} {1}'.format(repo, path)).failed:
            abort(red(u'Can\'t clone source code!'))
    print(green(u'Source code successfully cloned.'))


# Sublime


@task
def subl_init_project(name, path=env.project['root']):
    """ Set name of Sublime Text project root file to current project name.

    Args:
        name (str): Name of new project.
        path (str): Path to new project, defaults to '~/work'.
    """
    path = _path_abs(path)
    with cd(path):
        run('mv example.sublime-project {0}.sublime-project'.format(name))


# Teamocil


@task
def mk_teamocil_item(name, path=env.project['root']):
    """Create Teamocil item for new project.

    See https://github.com/remiprev/teamocil.

    Replace example patterns in project's file '.teamocil.yml'.
    After create symbol link of this file in '~/.teamocil/'.

    Args:
        name (str): Name of new project.
        path (str): Path to new project, defaults to '~/work'.
    """
    path = _path_abs(path)
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


# Meta tasks


@task
def mk_proj(name=None, path=env.project['root']):
    """Create new project.

    Args:
        name (unicode): Name of new project, defaults to None.
        path (str): Path to new project, defaults to '~/work'.

    Returns:
        Dict with project options: name, path and etc.
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
        mk_teamocil_item(**project)
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
    return project
