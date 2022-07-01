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

You can also configure overrides for certain commands by editing
~/.config/installcmd/overrides.yml. This has the same syntax as the package's own
commands.yaml file - indeed, it gets merged on top of that dictionary. To get a sample,
you can use the generate-overrides subcommand.

Usage:
    installcmd (-h|--help)
    installcmd [options]
    installcmd refresh [options]
    installcmd noninteractive [options]
    installcmd query [options]
    installcmd pkgspec YAML_PATH [options]
    installcmd generate-overrides

Options:
    --log LEVEL  Minimum level of logs to print [default: INFO]
"""
import logging
import shutil

from docopt import docopt
from metovlogs import get_log

from installcmd import BASE_SPEC_PATH, OVERRIDES_PATH
from installcmd.lib import install_pkg_command, load_yaml, simple_command

log = get_log(__name__)


def main():
    args = docopt(__doc__)

    loglvl = args["--log"]
    if loglvl:
        log.setLevel(logging.getLevelName(loglvl.upper()))

    if args["refresh"]:
        print(simple_command("refresh"))
    elif args["noninteractive"]:
        print(simple_command("noninteractive"))
    elif args["query"]:
        print(simple_command("query"))
    elif args["pkgspec"]:
        print(install_pkg_command(load_yaml(args["YAML_FILE"])))
    elif args["generate-overrides"]:
        generate_overrides()
    else:
        print(simple_command("install"))


def generate_overrides():
    if OVERRIDES_PATH.exists():
        log.critical(
            f"There's already a file at {OVERRIDES_PATH}. "
            "Delete it first if you don't want to keep it."
        )
        exit(1)

    log.info(f"Creating sample overrides file at {OVERRIDES_PATH}")
    shutil.copy(BASE_SPEC_PATH, OVERRIDES_PATH)
