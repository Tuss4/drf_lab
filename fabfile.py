from fabric.api import local, env, cd, run, sudo


env.hosts = ['ec2-54-191-20-55.us-west-2.compute.amazonaws.com']
env.user = 'ubuntu'
env.key_filename = '/vagrant/codelabtj.cer'

def test():
    local("./manage.py test")


def commit():
    local("git add -p && git commit")


def push():
    local("git push origin master")


def deploy():
    code_dir = '/home/ubuntu/drf_lab'
    with cd(code_dir):
        sudo("service figexample-run stop")
        run("git pull origin master")
        sudo("service figexample-run start")


def prepare_deploy():
    test()
    commit()
    push()
