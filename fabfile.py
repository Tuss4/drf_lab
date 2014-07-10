from fabric.api import *


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


# try:
#     from figexample.aws_settings import (AWS_STORAGE_BUCKET as tj_bucket,
#                                         AWS_SECRET_ACCESS_KEY as aws_s_key,
#                                         AWS_ACCESS_KEY_ID as aws_a_key_id,)
# except ImportError:
#     print "No AWS Settings."


aws_key = os.getenv("AWS_SECRET_ACCESS_KEY", "")
aws_a_id = os.getenv("AWS_SECRET_ACCESS_KEY_ID", "")

# BUCKET = 'vokalcodelabtj'
IP = '54.191.128.4'  # Elastic IP
REGION = 'us-west-2'


def staging():
    env.hosts = [IP,]
    env.user = 'ubuntu'
    env.branch = 'master'


def get_ec2_connection():
    return ec2.connect_to_region("us-west-2",
        aws_access_key_id=aws_a_id,
        aws_secret_access_key=aws_key)


def get_git_hash():
    return local("git rev-parse --short HEAD", capture=True)


def create_snapshot():
    conn = get_ec2_connection()
    all_inst = conn.get_all_instances()
    img_id = conn.get_all_addresses([IP,])[0].instance_id
    git_hash = local("git rev-parse --short HEAD")
    name = 'codelabtj-{0}-{1}'.format(date.today().isoformat(),
                                      get_git_hash())
    print "Snapshopt [{0}] has been created.".format(name)
    return conn.create_image(img_id, name, no_reboot=True)


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
    require("hosts", provided_by=[staging,])
    code_dir = '/home/ubuntu/drf_lab'
    with cd(code_dir):
        sudo("service codelabtj stop")
        run("git pull origin {0}".format(env.branch))
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
