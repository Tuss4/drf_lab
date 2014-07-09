from fabric.api import local, env, cd, run, sudo, prefix


import boto
from boto import s3, ec2
from boto.s3.key import Key
from figexample.settings import ALLOWED_HOSTS


import os
import sys
import glob
import mimetypes
from datetime import date


try:
    from figexample.settings_vm import (AWS_STORAGE_BUCKET as tj_bucket,
                                        AWS_SECRET_ACCESS_KEY as aws_s_key,
                                        AWS_ACCESS_KEY_ID as aws_a_key_id,)
except ImportError:
    print "No VM Settings."


env.hosts = [ALLOWED_HOSTS[1]]
env.user = 'ubuntu'
env.key_filename = '/vagrant/codelabtj.cer'

# BUCKET = 'vokalcodelabtj'
IP = '54.186.105.150'
REGION = 'us-west-2c'


def get_ec2_connection():
    return ec2.connect_to_region(REGION,
        aws_access_key_id=aws_a_key_id,
        aws_secret_access_key=aws_s_key)


def create_snapshot():
    conn = get_ec2_connection
    instance_id = conn.get_all_addresses([IP,])[0].instance_id
    git_hash = local("git rev-parse HEAD")
    name = 'codelabtj-{0}-{1}'.format(date.today().strftime("%m-%d-%y"),
                                      git_hash)
    return conn.create_image(instance_id, name, no_reboot=True)


def test():
    local("./manage.py test")


def commit():
    local("git add -p && git commit")


def push():
    local("git push origin master")


def upload_file(f, root_path):
    """
    Will only work if you're on the
    EC2 Instance.
    """
    conn = boto.connect_s3(aws_a_key_id, aws_s_key)
    k = Key(bucket=conn.get_bucket(tj_bucket))
    k.key = '{0}/{1}'.format(root_path, f.name)
    k.set_metadata('Content-Type', mimetypes.guess_type(f.name)[0])
    k.set_contents_from_file(f)
    k.set_acl('public-read')


def upload():
    origin = os.getcwd()
    os.chdir("static")
    for f in glob.glob("*.html"):
        with open(f, 'r') as file_obj:
            upload_file(file_obj, '/')

    os.chdir(origin)
    os.chdir("static/admin/css/")
    for f in glob.glob("*.css"):
        with open(f, 'r') as file_obj:
            upload_file(file_obj, '/admin/css')

    os.chdir(origin)
    os.chdir("static/admin/img/")
    for f in glob.glob("*.gif"):
        with open(f, 'r') as file_obj:
            upload_file(file_obj, '/admin/img')
    for f in glob.glob("*.png"):
        with open(f, 'r') as file_obj:
            upload_file(file_obj, '/admin/img')

    os.chdir(origin)
    os.chdir("static/admin/img/gis")
    for f in glob.glob("*.png"):
        with open(f, 'r') as file_obj:
            upload_file(file_obj, '/admin/img/gis')

    os.chdir(origin)
    os.chdir("static/admin/js")
    for f in glob.glob("*.js"):
        with open(f, 'r') as file_obj:
            upload_file(file_obj, '/admin/js')

    os.chdir(origin)
    os.chdir("static/admin/js/admin")
    for f in glob.glob("*.js"):
        with open(f, 'r') as file_obj:
            upload_file(file_obj, '/admin/js/admin')

    os.chdir(origin)
    os.chdir("static/rest_framework/css/")
    for f in glob.glob("*.css"):
        with open(f, 'r') as file_obj:
            upload_file(file_obj, '/rest_framework/css')

    os.chdir(origin)
    os.chdir("static/rest_framework/img/")
    for f in glob.glob("*.png"):
        with open(f, 'r') as file_obj:
            upload_file(file_obj, '/rest_framework/png')

    os.chdir(origin)
    os.chdir("static/rest_framework/js/")
    for f in glob.glob("*.js"):
        with open(f, 'r') as file_obj:
            upload_file(file_obj, '/rest_framework/js')


def deploy():
    code_dir = '/home/ubuntu/drf_lab'
    with cd(code_dir):
        sudo("service codelabtj stop")
        run("git pull origin master")
        with prefix(". env/bin/activate"):
            run("./env/bin/python manage.py migrate")
            run("echo $PATH")
            run('deactivate')
        sudo("service codelabtj start")
    create_snapshot()


def prepare_deploy():
    test()
    commit()
    push()
