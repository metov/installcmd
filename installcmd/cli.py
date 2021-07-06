"""
Print the correct command for installing a package on the current system. The main
purpose of this is portability of install scripts across systems.

Supported commands:
* No argument -- prints install command eg. apt-get install
* refresh -- update package cache refresh command eg. apt-get update
* noninteractive -- answer all prompts yes eg. apt-get install -y
* pkgspec -- command to install specific package based on a YAML spec (see below)

For pkgspec, you need to pass the path to a package spec in YAML format with the
following structure:

    name: "generic-package-name"
    linux:
        name: "linux-name-of-package"
        arch:
            name: "arch-package-name"

        debian:
            name: "debian-package-name"
            buster:
                name: "buster-package-name"

This is a mechanism for dealing with situations where the same package is listed under
different names in different package managers. The most specific package name will be
preferred; in this case the "arch-package-name" will be preferred over
"generic-package-name" on Arch and "buster-package-name" will be preferred on Debian
buster (on other releases, "debian-package-name" will be preferred).

Usage:
    installcmd (-h|--help)
    installcmd [options]
    installcmd refresh [options]
    installcmd noninteractive [options]
    installcmd pkgspec YAML_PATH [options]

Options:
    --log LEVEL  Minimum level of logs to print [default: INFO]
"""
import logging

from docopt import docopt

from installcmd import log
from installcmd.lib import install_pkg_command, load_yaml, simple_command


def main():
    args = docopt(__doc__)

    loglvl = args["--log"]
    if loglvl:
        log.setLevel(logging.getLevelName(loglvl.upper()))

    if args["refresh"]:
        print(simple_command("refresh"))
    elif args["noninteractive"]:
        print(simple_command("noninteractive"))
    elif args["pkgspec"]:
        print(install_pkg_command(load_yaml(args["YAML_FILE"])))
    else:
        print(simple_command("install"))
