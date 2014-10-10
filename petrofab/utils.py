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

# Order is important
DEFAULT_CONFIGS = [
    '.petrofab/config.json',
    '.petrofab.json',
    '~/.petrofab/config.json',
]


def path_abs(path, check=True):
    """Return absolute path for some destination.

    Args:
        path (str): some path.
        check (bool): check path exists, default is True.

    Return:
        String is containing absolute path of arg 'path'.
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
        fabenv : Object 'env' from Fabric.
        path (str): Some path to config file, defaults None.

    Return:
        Updated object 'env' from Fabric.
    """
    if path is None:
        for config in DEFAULT_CONFIGS:
            _path = path_abs(config, False)
            if os.path.isfile(_path):
                path = _path
                break
    _path = path or prompt(u'Path to config:')
    _path = path_abs(_path)
    if not os.path.isfile(_path):
        abort(red(u'Config "{0}" not exists!').format(_path))
    config = json.load(open(_path))
    for key, value in config.iteritems():
        setattr(fabenv, key, value)
    return fabenv
