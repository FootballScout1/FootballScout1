#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the static
folder of the FootballScout1 project
"""

from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/football_scout_static_{}.tgz".format(date)
        local("tar -cvzf {} static".format(file_name))
        return file_name
    except BaseException:
        return None
