"""
Print the correct command for installing a package on the current system. The main
purpose of this is portability of install scripts across systems.

With no arguments, prints install command (eg. "sudo apt install") so you can
concatenate the package name yourself.

If you pass a filename, it is assumed to be a package spec in YAML format with the
following structure:

    name: "generic-package-name"
    Linux:
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
    install-cmd.py (-h|--help)
    install-cmd.py
    install-cmd.py update
    install-cmd.py pkgspec PKG_INFO
"""
from docopt import docopt

from lib import install_command, load_yaml, update_command


def main():
    args = docopt(__doc__)

    if args["update"]:
        print(update_command())
    elif args["pkgspec"]:
        print(install_command(load_yaml(args["PKG_INFO"])))
    else:
        print(install_command())
