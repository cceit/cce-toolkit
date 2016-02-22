from __future__ import with_statement
from warnings import warn

from fabric.operations import sudo
from fabric.api import run
from fabric.state import env


def pick():
    """
    Select which server(role) to execute the commands on
    """
    set_role(raw_input("%s \n Choose target (enter number):" % '\n'.join('%s : %s' % (k, v)
                                                                         for k, v in enumerate(env.roledefs))))


def dev():
    """
    Sets remote server to dev
    """
    set_role(role_name='dev')


def uat():
    """
    Sets remote server to uat
    """
    set_role(role_name='uat')


def prod():
    """
    Sets remote server to prod
    """
    set_role(role_name='prod')


def __confirm(warning):
    response = raw_input(warning + '\n are you sure you want to continue Y/N: ')
    if response.upper() in ['Y', 'YES']:
        return True
    return False


def __exec_cmd(command):
    run(command)


def __exec_setup_cmd(command):
    if env.role['production']:
        run(command)
    else:
        sudo(command)


def set_role(role_id=None, role_name=None):
    if not role_id and not role_name:
        exit('Bad arguments, no role id or role name given')
    try:
        if role_id:
            role = dict(enumerate(env.roledefs))[int(role_id)]
        else:
            role = role_name
    except (KeyError, ValueError):
        warn('The number you selected does not exist, try again')
        pick()
    else:
        env.role = env.roledefs[role]
        env.hosts = [env.role['server']]
