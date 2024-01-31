#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers."""
from os.path import exists
from fabric.api import put, run, env

env.hosts = ['52.87.19.225', '54.160.68.241']


def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    if not exists(archive_path):
        return False
    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress archive to /data/web_static/releases/
        file_name = archive_path.split("/")[-1]
        path = "/data/web_static/releases/{}".format(file_name.split(".")[0])
        run(f"mkdir -p {path}")
        run(f"tar -xzf /tmp/{file_name} -C {path}")

        # Delete the archive from the web server
        run(f"rm /tmp/{file_name}")

        # Move the files after extraction
        run(f"mv {path}/web_static/* {path}/")

        # Delete empty web_static directory
        run(f"rm -rf {path}/web_static")

        # Delete the symbolic link /data/web_static/current from web server
        run('rm -rf /data/web_static/current')

        # Create new link /data/web_static/current linked to the new version
        run(f"ln -s {path}/ /data/web_static/current")

        return True
    except Exception:
        return False
