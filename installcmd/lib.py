import platform
from pathlib import Path
from typing import Dict, Union

import yaml

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
        raise Exception("Could not find valid install command.")

    if pkg_spec is None:
        return install

    # If package spec is given, handle that as well
    package = apply_spec(pkg_spec, "name")
    if package is None:
        raise Exception("Could not find valid package name.")

    return f'{install} {package}'


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
    # Read OS, distribution and release

    u = platform.uname()

    # Default value
    res = spec.get(key, None)

    # Per-OS value
    d_os = spec.get(u.system, {})
    res = d_os.get(key, res)

    # Per-distro value
    d_dist = d_os.get(u.node, {})
    res = d_dist.get(key, res)

    # Per release value
    d_rls = d_dist.get(u.release, {})
    res = d_rls.get(key, res)

    return res


def load_yaml(yaml_path: str):
    with open(yaml_path) as f:
        y = yaml.safe_load(f)
    return y
