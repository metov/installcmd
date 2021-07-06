import platform
from pathlib import Path
from typing import Dict, Union, List

import yaml

from installcmd import log, linux

RELEASE_SPEC = Dict[str, str]
DISTRO_SPEC = Dict[str, Union[str, RELEASE_SPEC]]
OS_SPEC = Dict[str, Union[str, DISTRO_SPEC]]


def install_pkg_command(pkg_spec: Dict[str, OS_SPEC]) -> str:
    """
    Return correct command for installing a package on this system, according to the
    given spec. If it can't find a common, will exit with non-zero exit code.

    :param pkg_spec: A parsed package spec
    """

    cmd_spec = load_yaml(Path(__file__).parent / "commands.yaml")
    install = apply_spec(cmd_spec, "install")
    if install is None:
        log.error(f"No known install command for this platform")
        exit(1)

    # If package spec is given, handle that as well
    package = apply_spec(pkg_spec, "name")
    if package is None:
        raise Exception("Could not find valid package name.")

    return f"{install} {package}"


def simple_command(cmd_name: str) -> str:
    """
    Return requested command for this platform. If spec fails to match any commands at
    all, will exit with non-zero code.
    """
    cmd_spec = load_yaml(Path(__file__).parent / "commands.yaml")
    command = apply_spec(cmd_spec, cmd_name)
    if command is None:
        log.error(f"Could not find valid {cmd_name} command.")

    return command


def apply_spec(spec: Dict[str, OS_SPEC], key: str) -> str:
    """
    Search through spec and return most specific matching value, if any.

    The implementation uses os/distro/release terminology, which is Linux-specific.
    However we are actually calling Python's platfrom uname, node and release which
    should be platform independent (at least in theory). Since Linux OSes have
    vastly more version diversity, there's not really a commonly used Kernel-agnostic
    terminology, so I decided to just pretend the Linux terms apply to all OSes. Again,
    this is a matter of comments and variable names, as the code itself is meant
    to be OS-agnostic.
    """
    # Try looking for successively less qualified commands
    path = [os_name(), distro_name(), platform.uname().release]
    while path:
        full_path = path + [key]
        str_path = "/".join(full_path)
        release_cmd = dict_get_path(spec, full_path)
        if release_cmd:
            log.info(f'Found "{release_cmd}" at {str_path}')
            return release_cmd
        log.debug(f"Couldn't find key: {str_path}")
        path.pop()

    # At this point, you would return an OS-independent generic command, but if
    # such a thing existed this package would not be necessary :)
    log.error(f"Couldn't match this platform. Returning None.")
    return None


def os_name():
    # In Docker containers, uname returns host's OS name
    if linux.is_linux():
        return "linux"
    else:
        return platform.uname().system


def distro_name():
    if linux.is_linux():
        return linux.distro_name()
    else:
        return platform.uname().node


def dict_get_path(d: dict, key_path: List[str]):
    """
    Descend down the path of keys in the dictionary and retrieve value. If not
    found, return None.
    """
    for k in key_path:
        if k not in d:
            return None
        d = d[k]
    return d


def load_yaml(yaml_path: str):
    with open(yaml_path) as f:
        y = yaml.safe_load(f)
    return y
