#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers.
"""
from datetime import datetime
from os.path import isdir, exists
from fabric.api import put, run, env, local

env.hosts = ['52.87.19.225', '54.160.68.241']


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


def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    if not exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')

        file_name = archive_path.split("/")[-1]
        path = "/data/web_static/releases/{}".format(file_name.split(".")[0])
        run(f"mkdir -p {path}")
        run(f"tar -xzf /tmp/{file_name} -C {path}")

        run(f"rm /tmp/{file_name}")

        run(f"mv {path}/web_static/* {path}/")
        run(f"rm -rf {path}/web_static")
        run('rm -rf /data/web_static/current')

        run(f"ln -s {path}/ /data/web_static/current")

        return True
    except Exception:
        return False


def deploy():
    """Creates an archive and distributes to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
