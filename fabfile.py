import os
from contextlib import contextmanager
from fabric.api import cd, env, prefix, run, sudo, task
from fabric.context_managers import shell_env


PROJECT_NAME = 'mapala'
PROJECT_ROOT = '/var/www/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, '.env')

env.hosts = []


@task
def production():
    env.hosts = ['root@158.69.210.48']
    env.environment = 'production'
    env.NODE_ENV = 'production'
    env.brunch = 'master'


@task
def develop():
    env.hosts = ['root@37.59.98.17']
    env.environment = 'development'
    env.NODE_ENV = 'development'
    env.brunch = 'dev'


@contextmanager
def source_virtualenv():
    with prefix('source ' + os.path.join(VENV_DIR, 'bin/activate')):
        yield


def chown():
    """Sets proper permissions"""
    sudo('chown -R www-data:www-data %s' % PROJECT_ROOT)


@task
def test():
    with shell_env(NODE_ENV='production'):
        sudo('echo $NODE_ENV')


@task
def restart():
    # sudo('systemctl restart nginx')
    sudo('systemctl restart mapala')
    sudo('systemctl restart mapala_fetch')


@task
def fetch(blockchain):
    with cd(PROJECT_ROOT):
        with source_virtualenv():
            run('./manage fetch %s' % blockchain)


@task
def deploy_only_back():
    with cd(PROJECT_ROOT):
        run('git pull origin %s --no-edit' % env.brunch)
        with source_virtualenv():
            run('source .env/bin/activate && pip install -r requirements.txt')
            run('./manage collectstatic --noinput')
            run('./manage migrate')

    restart()


@task
def deploy():
    """
    Deploys the latest tag to the production server
    """
    # sudo('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        run('git pull origin %s --no-edit' % env.brunch)
        with source_virtualenv():
            run('source .env/bin/activate && pip install -r requirements.txt')
            run('./manage collectstatic --noinput')
            run('./manage migrate')

    restart()
