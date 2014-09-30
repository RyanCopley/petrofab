# -*- coding: utf-8 -*-
# native
import json
import os
import sys

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
    """
    path = os.path.expanduser(path)
    path = os.path.normcase(path)
    path = os.path.normpath(path)
    path = os.path.abspath(path)
    if check and not os.path.exists(path):
        msg = u'Path "%s" not exists!' % path.decode(sys.stdin.encoding)
        msg = msg.encode(sys.stdout.encoding)
        abort(red(msg))
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
