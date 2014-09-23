# -*- coding: utf-8 -*-
# native
import json
import os
import sys

# fabric.api
from fabric.colors import red
from fabric.utils import abort

# fabric.contrib
from fabric.contrib.files import exists

__all__ = [
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
    if check and not exists(path):
        msg = u'Path "%s" not exists!' % path.decode(sys.stdin.encoding)
        msg = msg.encode(sys.stdout.encoding)
        abort(red(msg))
    return path


def get_config(path=None):
    """Get config data from config file.

    Read JSON config file and convert data to Python dict.

    Args:
        path (str): Some path to config file,
                    defaults 'petrofab/defaults.json'.
    """
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, 'defaults.json')
    path = path_abs(path)
    config = json.load(open(path).read())
    return config
