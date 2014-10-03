[![Build Status](https://travis-ci.org/petrikoz/petrofab.svg?branch=develop)](https://travis-ci.org/petrikoz/petrofab)
[![Coverage Status](https://img.shields.io/coveralls/petrikoz/petrofab/develop.svg)](https://coveralls.io/r/petrikoz/petrofab?branch=develop)

# petrofab #

Utilities for work projects. Based on [Fabric](https://github.com/fabric/fabric).

## Install ##

```shell
pip install git+https://github.com/petrikoz/petrofab.git
```

## Usage ##

Place your `fabfile.py` in any directory:

```python
# -*- coding: utf-8 -*-
# native
import os

# fabric.api
from fabric.api import env
from fabric.colors import cyan
from fabric.decorators import task
from fabric.operations import prompt

# fabric.contrib
from fabric.contrib.console import confirm

# petrofab
from petrofab.project import Project
from petrofab.sublime import Sublime
from petrofab.teamocil import Teamocil
from petrofab.utils import get_config

current_path = os.path.dirname(os.path.abspath(__file__))

# Fabric environment
env = get_config(env, current_path)


@task
def mk_proj(name=None, path=None):
    """Create new project.

    Args:
        name (str): Name of new project, defaults to None.
        path (str): Path to new project, defaults to None.
    """
    _project = getattr(env, 'project', {})
    _name = name or _project.get('name') or prompt(u'Project name:')
    _path = path or _project.get('path') or prompt(u'Path to project:')
    project = Project(_name, _path, project=_project)
    project.make_path()
    project.get_template()
    project.clean()
    msg = (u'\nProject was create:'
           u'\n\tName:\t{project.name}'
           u'\n\tPath:\t{project.path}')
    if project.url:
        msg += u'\n\tTemplate:\t{project.url}'
    # Source code
    if confirm(u'Clone source code to project?', default=False):
        project.get_source_code()
        msg += u'\n\tSource code:\t{project.src}'
    sublime = Sublime(project.name, project.path)
    sublime.make_project()
    # Teamocil
    if confirm(u'Init Teamocil?', default=False):
        _teamocil = getattr(env, 'teamocil', {})
        teamocil = Teamocil(project.path, name=project.name,
                            teamocil=_teamocil)
        teamocil.init_layout()
        teamocil.enable_layout()
        msg += u'\n\tTeamocil layout:\t{.name}'.format(teamocil)
    msg = msg.format(project=project)
    print(cyan(msg))


@task
def del_proj(name=None, path=None):
    """Remove exist project.

    Args:
        name (str): Name of project, defaults to None.
        path (str): Path to project, defaults to None.
    """
    _name = name or prompt(u'Project name:')
    _path = path or prompt(u'Path to project:')
    project = Project(_name, _path)
    project.remove()
    _teamocil = getattr(env, 'teamocil', {})
    teamocil = Teamocil(_path, teamocil=_teamocil)
    teamocil.disable_layout(name)
```


Optionaly your can place `.petrofab.json` in there.

```json
{
  "hosts": ["localhost"],
  "project": {
    "path": ".",
    "url": "https://github.com/petrikoz/project-template.git"
  },
  "teamocil": {
    "root": "~/.teamocil",
    "filename": ".teamocil.yml"
  }
}
```

Run any task:

```shell
fab mk_proj:foo,/tmp
```
