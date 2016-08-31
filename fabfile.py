from fabric.contrib.project import rsync_project
from fabric.api import local, run, env, sudo, hide, settings, put
from fab_config import PRODUCTION_USER, PRODUCTION_HOST, PRODUCTION_PASSWORD



env.roledefs = {'production' : ['%s@%s'%(PRODUCTION_USER, PRODUCTION_HOST)],

}

default_password = PRODUCTION_PASSWORD


def ping(dst, count=5):
    check_password()

    if dst in hosts:
        dst  = hosts[dst]
    else:
        dst = dst

    run('ping %s -c %s'%(dst, count))


def check_password():
    if default_password == '':
        passwd = getpass.getpass('Enter your password: ')
    else:
        passwd = default_password

    env.passwords = {'%s@%s:22'%(PRODUCTION_USER, PRODUCTION_HOST) : passwd,
                    }

def deploy():
    check_password()
    rsync_project(remote_dir = 'salicapi/', local_dir = '../salicapi/')
    sudo('cd /home/%s/salicapi/ && sh install.sh'%(PRODUCTION_USER))
    sudo("cd /opt/salic/salic-api && find . -name '*.pyc' -delete")
    put('salic-api/app/deployment.cfg', '/opt/salic/salic-api/app/deployment.cfg', use_sudo=True)
    sudo('/etc/init.d/salic-api start')


def date():
    check_password()
    run('date')

def command(com, su = 'False'):
    check_password()
    if su == 'False':
        run (com)
    else:
        sudo (com)

def test():
    local('ls')
