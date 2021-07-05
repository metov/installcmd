"""
Linux-specifc OS detection methods.
"""
import dotenv
from pathlib import Path
from installcmd import log


def osrel():
    return Path("/etc/os-release")


def lsbrel():
    return Path("/etc/lsb-release")


def is_linux():
    """
    Return true (hopefully) if OS is Linux.

    TODO: Handle corner cases as they arise.
    """
    if osrel().exists() or lsbrel().exists():
        return True

    return False


def distro_name():
    # /etc/os-release is more reliable than uname eg. in Docker containers
    # See also https://unix.stackexchange.com/q/92199
    if osrel():
        osrel_file = dotenv.dotenv_values(osrel())
        return osrel_file["ID"]
    log.warning("Couldn't find distro name.")
    return None
