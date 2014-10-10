# -*- coding: utf-8 -*-
# native
import os

# fabric.api
from fabric.api import env
from fabric.colors import cyan, green, red
from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import prompt, run
from fabric.tasks import Task
from fabric.utils import abort

# fabric.contrib
from fabric.contrib.console import confirm

# in-module
from .utils import path_abs

__all__ = [
    'disable_layout',
    'enable_layout',
    'init_layout',
    'mk_layout',
]

env.hosts = ['localhost']

TEAMOCIL_ROOT = '~/.teamocil'
TEAMOCIL_LAYOUT_CONFIG = '.teamocil.yml'


def _get_layout(path, filename=TEAMOCIL_LAYOUT_CONFIG):
    """Make path to layout config.

    Args:
        path (str): Path to folder which contains layout config.
        filename (str): Filename layout config, defaults to '.teamocil.yml'.

    Return:
        Absolute path to layout config file.
    """
    layout = os.path.join(path, filename)
    if not os.path.isfile(layout):
        abort(red('"%s" not exists!' % layout))
    return layout


@task
def init_layout(name, path, filename=TEAMOCIL_LAYOUT_CONFIG):
    """Replace examples patterns in specific teamocil config.

    Args:
        name (str): Layout name.
        path (str): Path to folder which contains layout config.
        filename (str): Filename layout config, defaults to '.teamocil.yml'.
    """
    _name = name.lower()
    _path = path_abs(path)
    layout = _get_layout(_path, filename)
    repls = (
        ('<example>', _name),
        ('<Example>', _name.title()),
        ('<example/path>', _path),
    )
    with cd(_path):
        for repl in repls:
            run('sed -i.bak -e \'s|{0}|{1}|g\' {file}'.format(*repl,
                                                              file=layout))
    print(green('Teamocil layout in "{0}" was init.').format(layout))
    return layout


@task
def enable_layout(name, path, root=TEAMOCIL_ROOT,
                  filename=TEAMOCIL_LAYOUT_CONFIG):
    """Make Teamocil layout in Teamocil root folder.

    Args:
        name (str): Layout name.
        path (str): Path to folder which contains layout config.
        filename (str): Filename layout config, defaults to '.teamocil.yml'.
        root (str): Teamocil root folder, defaults to '~/.teamocil'.
    """
    _name = name.lower()
    _path = path_abs(path)
    _root = path_abs(root)
    link = os.path.join(_root, '%s.yml' % _name)
    layout = _get_layout(_path, filename)
    run('ln -s {0} {1}'.format(layout, link))
    print(green('Teamocil layout "{0}" enabled.').format(_name))


@task
def disable_layout(name, root=TEAMOCIL_ROOT):
    """Disable exist Teamocil layout.

    Args:
        name (str): Layout name.
        root (str): Teamocil root folder, defaults to '~/.teamocil'.
    """
    _name = name.lower()
    _root = path_abs(root)
    link = os.path.join(_root, '%s.yml' % _name)
    run('rm -f {0}'.format(link))
    print(green('Teamocil layout "{0}" disabled.').format(_name))


class TeamocilTask(Task):

    """Full task for create new Teamocil layout."""

    name = 'mk_layout'

    def run(self, name=None, path=None, config={}, root=None, filename=None):
        self.env = config or getattr(env, 'teamocil', {})
        self.layout_name = name or prompt('Teamocil layout name:')
        self.layout_path = path or prompt('Path to Teamocil layout config:')
        _file = filename or self.env.get('filename', None)
        self.layout_file = _file or prompt('Teamocil layout config:')

        layout = init_layout(self.layout_name, self.layout_path,
                             self.layout_file)
        if confirm('Enable layout?'):
            _root = root or self.env.get('root', None)
            self.teamocil_root = _root or prompt('Teamocil root folder:')
            enable_layout(self.layout_name, self.layout_path,
                          self.teamocil_root, self.layout_file)
            msg = ('\nTeamocil layout inited:'
                   '\n\tName:\t{0.layout_name}'
                   '\n\tConfig:\t{1}')
            print(cyan(msg.format(self, layout)))

mk_layout = TeamocilTask()
