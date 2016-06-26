from __future__ import with_statement
import os

from fabric.context_managers import cd
from fabric.state import env
from .environment import __exec_cmd

join = os.path.join


def git_pull():
    """
    runs git pull in the project directory of the selected role
    """
    with cd(env.role['project_dir']):
        __exec_cmd('git pull')


def git_checkout(branch):
    """
    runs git checkout branch in the project directory of the selected role
    """
    with cd(env.role['project_dir']):
        __exec_cmd('git checkout %s' % branch)
