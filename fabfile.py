import contextlib
from fabric.api import *
from fabric.contrib.files import exists

try:
    from local_fabfile import *
except ImportError:
    pass

# globals

env.project_name = 'tbdd'

@contextlib.contextmanager
def target_user(subdir=None):
    old_user = env.user
    env.user = env.target_user
    path = env.path
    if subdir:
        path += '/' + subdir
    with cd(path):
        yield
    env.user = old_user

# environments

def localvm():
    "Use the local virtual server"
    env.hosts = ['tbdd-dev.local:22']
    env.path = '/srv/tbdd'
    env.user = 'user'
    env.target_user = 'tbdd'
    env.virtualhost_path = "/configs/common/"

# tasks

def test():
    "Run the test suite and bail out if it fails"
    local("DEPLOYMENT_TARGET=development ./manage test")

def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    require('hosts', 'target_user', provided_by=[localvm])
    require('path')

    sudo('apt-get update')
    sudo('aptitude install -y git-core')
    sudo('aptitude install -y memcached')
    sudo('aptitude install -y python-setuptools')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('aptitude install -y apache2')
    sudo('aptitude install -y libapache2-mod-wsgi')
    # we want rid of the defult apache config
    sudo('cd /etc/apache2/sites-available/; a2dissite default;')
    sudo('mkdir -p %s' % env.path)
    sudo('chown {0}:{0} {1}'.format(env.target_user, env.path))
    with target_user():
        run('virtualenv .')
        run('bin/easy_install pip')
        run('mkdir -p releases shared packages')

def deploy():
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, install the virtual host and
    then restart the webserver
    """
    require('hosts', provided_by=[localvm])
    require('path')

    import time
    env.release = time.strftime('%Y%m%d%H%M%S')

    upload_tar_from_git()
    install_requirements()
    install_site()
    symlink_current_release()
    migrate()
    restart_webserver()

def deploy_version(version):
    "Specify a specific version to be made live"
    require('hosts', provided_by=[localvm])
    require('path')

    env.version = version
    with target_user():
        run('rm releases/previous')
        run('mv releases/current releases/previous')
        run('ln -s %s releases/current' % (env.version,))
    restart_webserver()

def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two,
    NOT keep going back in time.
    """
    require('hosts', provided_by=[localvm])
    require('path')

    with target_user():
        run('mv releases/current releases/_previous')
        run('mv releases/previous releases/current')
        run('mv releases/_previous releases/previous')
    restart_apache()

# Helpers. These are called by other functions rather than directly

def upload_tar_from_git():
    "Create an archive from the current Git master branch and upload it"
    require('release', provided_by=[deploy])
    release_tgz = '{0}.tar.gz'.format(env.release)
    local('git archive --format=tar master | gzip > {0}'.format(release_tgz))
    with target_user():
        run('mkdir -p releases/%s' % (env.release,))
        put(release_tgz, '{0}/packages/{1}'.format(env.path, release_tgz))
    with target_user('releases/{0}'.format(env.release)):
        run('tar xzf ../../packages/{0}'.format(release_tgz))
    local('rm {0}'.format(release_tgz))

def install_site():
    "Add the virtualhost file to apache"
    require('release', provided_by=[deploy])
    sudo('cd %s/releases/%s; cp %s%s%s /etc/apache2/sites-available/' % (env.path, env.release, env.project_name, env.virtualhost_path, env.project_name))
    sudo('cd /etc/apache2/sites-available/; a2ensite %s' % env.project_name)
    if not exists('/var/log/apache2/%s' % env.project_name):
        sudo('mkdir -p /var/log/apache2/%s' % env.project_name)

def install_requirements():
    "Install the required packages from the requirements file using pip"
    require('release', provided_by=[deploy])
    with target_user():
        run('cd releases/{0}; ../../bin/python setup.py develop'.format(env.release))
        run('pip install -E . -r releases/{0}/requirements.txt'.format(env.release))

def symlink_current_release():
    "Symlink our current release"
    require('release', provided_by=[deploy])
    with target_user():
        if exists('%s/releases/previous' % env.path):
            run('rm releases/previous')
        if exists('%s/releases/current' % env.path):
            run('mv releases/current releases/previous')
        run('ln -s %s releases/current' % (env.release,))

def migrate():
    "Update the database"
    require('project_name')
    with target_user():
        run('source bin/activate; DEPLOYMENT_TARGET=live releases/current/manage syncdb --migrate --noinput')

def restart_webserver():
    "Restart the web server"
    sudo('/etc/init.d/apache2 restart')
