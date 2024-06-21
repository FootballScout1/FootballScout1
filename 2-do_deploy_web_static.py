#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['142.44.167.228', '144.217.246.195']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
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
