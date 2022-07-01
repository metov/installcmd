"""
Mac-specifc OS detection methods.
"""
import platform
import subprocess

from metovlogs import get_log

log = get_log(__name__)


def is_mac():
    """
    Return true (hopefully) if OS is Linux.

    TODO: Handle corner cases as they arise.
    """
    if platform.uname().system == "Darwin":
        return "mac"

    return False


def package_manager():
    if is_brew():
        return "brew"

    log.warning("Couldn't detect package manager.")
    return None


def is_brew():
    """
    Return true if homebrew is installed.

    TODO: Handle corner cases as they arise.
    """
    res = subprocess.run(["brew", "--version"], capture_output=True)

    if res.returncode != 0:
        return False

    if "Homebrew" not in res.stdout.decode():
        return False

    return True
