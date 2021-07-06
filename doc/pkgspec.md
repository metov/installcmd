# Package specs
Installcmd relies on YAML files defining which command to use in what situation. Currently, it goes by:

* Platform (eg. Linux, MacOS)
* Distro (eg. Debian, Ubuntu)
* Release

Not all OSes have distros like Linux, but it's a useful terminology to distinguish different OSes, flavors of the same OS and mere versions of the same flavor. Note that package managers are usually per-distribution, while *package names* can be release-specific (eg. Debian stable vs. testing).

The YAML files are called specs and are shallow trees. There's a "special" spec (`commands.yaml`) that gets shipped with installcmd, defining the package manager commands for each platform (under `install`, `refresh`, etc. instead of `name` as for regular packages). There's not that many package managers and they don't change that much, so this is convenient to do. For individual packages, we let every user maintain their own specs for packages relevant to them, although they are encouraged to share them.

For an example of a package spec, see (`docker.yaml`)[../pkgspec/docker.yaml]. Due to an older package also called docker, the container framework Docker shows up as `docker.io` in Debian repos. By using the package spec you can normalize the install command:
```
# On Arch
$ installcmd pkgspec docker.yaml
sudo pacman -S docker

# On Ubuntu
$ installcmd pkgspec docker.yaml
sudo apt install docker.io
``` 

Note that there's a top-level `name` in `dockery.yaml`, so even on non-Linux systems installcmd will return `docker` (which is typically its name on non-Linux package managers like brew).
