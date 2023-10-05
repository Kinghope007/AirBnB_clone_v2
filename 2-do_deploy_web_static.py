#!/usr/bin/python3
"""
Fabric script that distributes an archive to
your web servers, using the function do_deploy.
"""
from fabric.api import *
from os.path import exists
from datetime import datetime


env.hosts = ['18.234.169.191', '54.157.177.231']


@task
def do_pack():
    """
    Create a .tgz archive from web_static folder.
    """
    try:
        current_time = datetime.utcnow()
        file_name = "web_static_{}.tgz".format(current_time.strftime(
            "%Y%m%d%H%M%S"))
        local("mkdir -p versions")
        local("tar -czvf versions/{} web_static".format(file_name))
        return "versions/{}".format(file_name)
    except Exception:
        return None


@task
def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split('/')[-1]
        archive_no_ext = archive_filename.split('.')[0]

        # Upload the archive to /tmp/
        put(archive_path, "/tmp/")

        # Create the folder /data/web_static/releases/<archive_no_ext>/
        run("mkdir -p /data/web_static/releases/{}/".format(archive_no_ext))

        # Uncompress the archive to /data/web_static/releases/<archive_no_ext>/
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            archive_filename, archive_no_ext))

        # Delete the archive from the server
        run("rm /tmp/{}".format(archive_filename))

        # Move the uncompressed files to the final destination
        run(
                "mv /data/web_static/releases/{}/web_static/* /data/"
                "web_static/releases/{}/".format(
                    archive_no_ext, archive_no_ext))

        run("rm -rf /data/web_static/releases/{}/web_static".format(
            archive_no_ext))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run(
                "ln -s /data/web_static/releases/{}/ /data/web_static/"
                "current".format(archive_no_ext))

        return True

    except Exception:
        return False
