#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers for FootballScout1
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['142.44.167.228', '144.217.246.195']


def do_pack():
    """Generates a tgz archive from the static folder"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = "versions/football_scout_static_{}.tgz".format(date)
        local("tar -cvzf {} static".format(file_name))
        return file_name
    except BaseException:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/football_scout/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/static'.format(path, no_ext))
        run('rm -rf /data/football_scout/current')
        run('ln -s {}{}/ /data/football_scout/current'.format(path, no_ext))
        return True
    except BaseException:
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
