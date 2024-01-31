#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""
from fabric.api import run, env, local, lcd, cd
import os

env.hosts = ['52.87.19.225', '54.160.68.241']


def do_clean(number=0):
    """Delete out-of-date archives."""
    number = max(int(number), 1)

    archive_list = sorted(os.listdir("versions"))
    archives_to_delete = archive_list[:-number]
    with lcd("versions"):
        for archive in archives_to_delete:
            local(f"rm ./{archive}")

    with cd("/data/web_static/releases"):
        archive_list = run("ls -tr").split()
        archive_list = [i for i in archive_list if "web_static_" in i]
        archives_to_delete = archive_list[:-number]
        for archive in archives_to_delete:
            run(f"rm -rf {archive}")
