import platform
from pathlib import Path
from typing import Dict, Union, List

import yaml

from installcmd import log

RELEASE_SPEC = Dict[str, str]
DISTRO_SPEC = Dict[str, Union[str, RELEASE_SPEC]]
OS_SPEC = Dict[str, Union[str, DISTRO_SPEC]]


def install_command(pkg_spec: Dict[str, OS_SPEC] = None) -> str:
    """
    Return correct install command for this system. If package spec is given, will
    also attempt to select appropriate package name from the spec. Otherwise will
    only return the install command.

    If either spec fails to match any commands/names at all, will crash.

    :param pkg_spec: A parsed package spec (optional)
    :return: Correct install command for this system.
    """

    cmd_spec = load_yaml(Path(__file__).parent / "commands.yaml")
    install = apply_spec(cmd_spec, "install")
    if install is None:
        log.error(f"No known install command for this platform")
        exit(1)

    if pkg_spec is None:
        return install

    # If package spec is given, handle that as well
    package = apply_spec(pkg_spec, "name")
    if package is None:
        raise Exception("Could not find valid package name.")

    return f"{install} {package}"


def update_command() -> str:
    """
    Return correct update (refresh package cache) command for this system. If spec
    fails to match any commands at all, will crash.

    :return: Correct update command for this system.
    """

    cmd_spec = load_yaml(Path(__file__).parent / "commands.yaml")
    update = apply_spec(cmd_spec, "update")
    if update is None:
        raise Exception("Could not find valid update command.")

    return update


def apply_spec(spec: Dict[str, OS_SPEC], key: str) -> str:
    """
    Read OS, distribution and release.

    The implementation uses os/distro/release terminology, which is Linux-specific.
    However we are actually calling Python's platfrom uname, node and release which
    should be platform independent (at least in theory). Since Linux OSes have
    vastly more version diversity, there's not really a commonly used Kernel-agnostic
    terminology, so I decided to just pretend the Linux terms apply to all OSes. Again,
    this is a matter of comments and variable names, as the code itself is meant
    to be OS-agnostic.
    """
    # Try looking for successively less qualified commands
    path = [platform.uname().system, distro_name(), platform.uname().release]
    while path:
        str_path = "/".join(path)
        release_cmd = dict_get_path(spec, path + [key])
        if release_cmd:
            log.info(f'Found "{release_cmd}" at {str_path}')
            return release_cmd
        log.debug(f"Couldn't find key: {str_path}")
        path.pop()

    # At this point, you would return an OS-independent generic command, but if
    # such a thing existed this package would not be necessary :)
    log.error(f"Couldn't match this platform. Returning None.")
    return None


def distro_name():
    # Doesn't work on Docker - instead, if Linux, check /etc/os-release
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
