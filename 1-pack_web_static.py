#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of AirBnB Clone repo.
"""
from fabric.api import local
from datetime import datetime
from os.path import isdir


def do_pack():
    """
    Generates a .tgz archive from the contents of web_static folder.
    """
    if isdir("versions") is False:
        local("mkdir versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"

    result = local(f"tar -cvzf {archive_path} web_static", capture=True)

    if result.succeeded:
        return archive_path
    else:
        return None
