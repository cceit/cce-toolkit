from .environment import __exec_cmd, __exec_setup_cmd
from .env_settings import project_name, git_link
from fabric.state import env
from .git_tools import git_checkout
from fabric.context_managers import cd


def setup_project():
    """
    Initial setup of service account, environment and repo
    """
    create_service_account(project_name)
    initial_project_deployment()


def create_service_account(account):
    """
    create service account, change password and set permissions
    """
    __exec_cmd('sudo adduser %s' % account)
    __exec_cmd('sudo passwd %s' % account)
    __exec_cmd('sudo chown %s:ssh-git /home/%s -R' % (account, account))


def initial_project_deployment():
    """
    setup project environment and repo
    """
    __exec_setup_cmd('rm -rf /home/%s/env' % project_name)
    __exec_setup_cmd('rm -rf /home/%s/app' % project_name)
    __exec_setup_cmd('virtualenv /home/%s/env --no-site-packages' % project_name)
    __exec_setup_cmd('git clone %s /home/%s/app' % (git_link, project_name))
    setup_permissions(project_name)
    with cd(env.role['project_dir']):
        __exec_setup_cmd('git config --global user.email "devs@cce.ou.edu"')
        __exec_setup_cmd('git config --global user.name "Server"')
    git_checkout(env.role['branch'])
    update_requirements()
    setup_permissions(project_name)


def setup_permissions(account):
    """
    setup project environment and repo
    """
    __exec_setup_cmd('setfacl -R -m g:apache:rwx /home/%s/ ' % account)
    __exec_setup_cmd('setfacl -R -m g:ssh-git:rwx /home/%s/ ' % account)
    __exec_setup_cmd('setfacl -R -m u:%s:rwx  /home/%s/ ' % (account, account))


def update_requirements():
    """
    pip installs the project requirements from requirements.txt
    """
    __exec_cmd('%s/bin/pip uninstall -y cce_toolkit' % (env.role['virtualenv']))
    __exec_cmd('%s/bin/pip install -r %s/requirements.txt' % (env.role['virtualenv'], env.role['requirements_path']))


def reload_http():
    """
    restarts the httpd server
    """
    __exec_cmd('sudo /sbin/service httpd reload')
