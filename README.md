# `installcmd`

> Print correct command for installing a package.

The main use of this tool is to increase the portability of package installation scripts, such as you might have in a dotfiles repo. 

## Installation
`pip install .` while in the repo root.

## Usage
Print generic install command:
```
$ installcmd
sudo apt install
```

Print command to update package cache:
```
$ installcmd update
sudo apt update
```

Print command to install specific package:
```
$ cat docker.yaml
name: docker
    linux:
        ubuntu:
            name: docker.io

# On Arch
$ installcmd pkgspec docker.yaml
sudo pacman -S docker

# On Ubuntu
$ installcmd pkgspec docker.yaml
sudo apt install docker.io
```

Execute command directly (use at your own risk!):
```
# Without spec
$ $(installcmd) package-name

# With spec
$ $(installcmd pkgspec docker.yaml)
```

## Package spec
Annoyingly, sometimes the same package has different names in the repositories of different OSes. For example, Docker is listed in most Linux distro as `docker`, but in Ubuntu it is `docker.io`. To solve this problem we can create a detailed spec of the package's names.

The spec is a YAML file defining a tree:
```yaml
name: "generic-package-name"
Linux:
  name: "linux-name-of-package"
  arch:
    name: "arch-package-name"
    
  debian:
    name: "debian-package-name"
    buster: 
      name: "buster-package-name"
    
  alpine:
    "3.12":
    name: "alpine-3.12-name"
``` 

`installcmd` will descend down this tree and use the value of `name` from the most specific matching node that has a `name`. In the example above:
* `generic-package-name` will be used on non-Linux systems
* On Arch Linux, `arch-package-name` will be preferred
* On Debian, `buster-package-name` will be preferred if buster, `debian-package-name` otherwise
* On Alpine 3.12 (but not other Alpines) `alpine-3.12-name` will be preferred
* On other Linux (including Alpine 3.11), `linux-name-of-package` will be preferred

The exact keys here come from Python's [`platform`](https://docs.python.org/3/library/platform.html) module. To find out yours, open a shell and run:
```shell script
python -c "import platform; print(platform.uname())"
```
You want the `system`, `node` and `release` attributes.

## Command spec
`commands.yaml` defines the actual package manager commands that `installcmd` knows. Its structure mimics the package spec, but instead of `name` we have:
* `install` for the installation command
* `update` for the package cache update command
