# -*- coding: utf-8 -*-
# fabric.api
from fabric.api import env
from fabric.colors import green
from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import prompt, run
from fabric.tasks import Task

# in-module
from .utils import path_abs

__all__ = [
    'rename',
    'subl_project',
]

env.hosts = ['localhost']


@task
def rename(new_name, path, old_name='example'):
    """ Set new name to Sublime project.

    Args:
        new_name (str): New name of Sublime project config file.
        path (str): Path to folder which contains Sublime project config file.
        old_name (str): Old name of Sublime project config file.
                        Default 'exapmle'.
    """
    _path = path_abs(path)
    with cd(_path):
        run(('mv {0}.sublime-project'
             ' {1}.sublime-project').format(old_name, new_name))
    print(green('Sublime project "{0}" named.').format(new_name))


class SublimeTask(Task):

    """Full task for create new Sublime project."""

    name = 'subl_project'

    def run(self, name=None, path=None, config={}):
        self.env = config or getattr(env, 'sublime', {})
        self.proj_name = name or prompt('Sublime project name:')
        self.proj_path = path or prompt('Path to Sublime project config:')
        rename(self.proj_name, self.proj_path)

subl_project = SublimeTask()
