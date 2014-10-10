# -*- coding: utf-8 -*-
# native
import os

# fabric.api
from fabric.api import env
from fabric.colors import cyan, green, red, yellow
from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import prompt, run
from fabric.tasks import Task

# fabric.contrib
from fabric.contrib.console import confirm

# in-module
from .utils import path_abs

__all__ = [
    'clean',
    'get_source_code',
    'get_template',
    'make_path',
    'mk_project',
    'ProjectTask',
    'remove_project',
]

env.hosts = ['localhost']


@task
def make_path(name, root):
    """Create directory for project.

    Args:
        name (str): Name of project.
        root (str): Path to folder which will contain new project.

    Return:
        Path to folder with new project: path + name.
    """
    _path = os.path.join(path_abs(root), name)
    run('mkdir -p {0}'.format(_path))
    print(green(u'"{0}" created.').format(_path))
    return _path


@task
def get_template(tmpl, path):
    """Clone template of project dirs.

    Clone template of project from GitHub:
    https://github.com/petrikoz/project-template

    Args:
        tmpl (str): URL to repo with project template.
        path (str): Path to project directory.
    """
    _path = path_abs(path)
    run('git clone {0} {1}'.format(tmpl, _path))
    print(green(u'"{0}" cloned.').format(tmpl))


@task
def clean(path, trash=['.git*', 'readme.*'], quiet=False):
    """Remove trash from cloned tmpl.

    Args:
        trash (list): List of patterns which will remove.
        quiet (bool): If True then warnings won't show. Default: False.
    """
    _path = path_abs(path)
    msg = yellow(u'Be careful! Clean operation can\'t cancel! Continue?')
    if not quiet and not confirm(msg):
        print(red(u'Canceled by user!'))
        return
    with cd(_path):
        for pattern in trash:
            run('find . -iname "%s" -print0 | xargs -0 rm -rf' % pattern)
    print(green(u'"{0}" is clean.').format(_path))


@task
def get_source_code(src, path):
    """Clone source code of project.

    Args:
        src (str): URL of repo with source code, defaults is None.
        path (str): Path to project folder.
    """
    _path = path_abs(os.path.join(path, 'src'))
    run('git clone {0} {1}'.format(src, _path))
    print(green(u'"{0}" cloned in "{1}".').format(src, _path))


@task
def remove_project(path):
    """Remove exist project by path."""
    msg = yellow(u'Be careful! Remove operation can\'t cancel! Continue?')
    if not confirm(msg):
        print(red(u'Canceled by user!'))
        return
    _path = path_abs(path, check=False)
    run('rm -rf {0}'.format(_path))
    print(green(u'Project "{0}" removed.').format(_path))


class ProjectTask(Task):

    """Full task for create new project."""

    name = 'mk_project'

    def run(self, name=None, root=None, config={}, tmpl=None, trash=None,
            src=None):
        self.env = config or getattr(env, 'project', {})

        self.proj_name = name or prompt(u'Project name:')
        _root = root or self.env.get('root', None)
        self.proj_root = _root or prompt(u'Project root path:')

        _tmpl = tmpl or self.env.get('tmpl', None)
        self.proj_tmpl = _tmpl or prompt(u'URL to repo with template:')

        self.trash = trash or self.env.get('trash', None)

        self.proj_path = make_path(self.proj_name, self.proj_root)
        get_template(self.proj_tmpl, self.proj_path)
        if self.trash is None:
            clean(self.proj_path, quiet=True)
        else:
            clean(self.proj_path, trash=self.trash, quiet=True)
        msg = (u'\nProject was create:'
               u'\n\tName:\t{project.proj_name}'
               u'\n\tPath:\t{project.proj_path}'
               u'\n\tTemplate:\t{project.proj_tmpl}')
        if confirm(u'Clone source code to project?', default=False):
            _src = src or self.env.get('src', None)
            self.proj_src = _src or prompt(u'Enter URL repo with source code:')
            get_source_code(self.proj_src, self.proj_path)
            msg += u'\n\tSource code:\t{project.proj_src}'
        print(cyan(msg.format(project=self)))

mk_project = ProjectTask()
