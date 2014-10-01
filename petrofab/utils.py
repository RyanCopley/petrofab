# -*- coding: utf-8 -*-
# native
import json
import os

# fabric.api
from fabric.colors import red
from fabric.operations import prompt
from fabric.utils import abort

__all__ = [
    'get_config',
    'path_abs',
]


def path_abs(path, check=True):
    """Return absolute path for some destination.

    Args:
        path (str): some path.
        check (bool): check path exists, default is True.

    Returns:
        String is containing absolute path of arg 'path'.

    Examples:
        Result must be absolute
        >>> path_abs('/./tmp')
        '/tmp'

        Result must exists
        >>> path_abs('/TmP')
        Traceback (most recent call last):
            ...
        SystemExit: 1
    """
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    if check and not os.path.exists(path):
        abort(red('Path "{0}" not exists!').format(path))
    return path


def get_config(fabenv, path=None):
    """Get config data from config file.

    Read JSON config file and convert data to Python dict.

    Args:
        path (str): Some path to config file,
                    defaults 'petrofab/defaults.json'.
    """
    _path = path or prompt(u'Path to config:')
    _path = path_abs(_path)
    if not os.path.isdir(_path):
        abort(red(u'"{0}" must be directory!').format(_path))
    _path = os.path.join(_path, '.petrofab.json')
    if not os.path.isfile(_path):
        abort(red(u'"{0}" not exists!').format(_path))
    config = json.load(open(_path))
    for key, value in config.iteritems():
        setattr(fabenv, key, value)
    return fabenv
