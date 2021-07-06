# `installcmd`

> Cross platform package install commands.

I use a lot of cross platform software. One annoying thing about it is that every platform has its own package manager with a unique install command. What's even worse is that sometimes the packages themselves are listed under slightly different names in different repositories. Installcmd solves this by detecting your platform and providing the correct command.  

## Installation
Install with: `pip install installcmd`

## Usage

* `installcmd` prints the install command, eg.: `apt-get install`
* `installcmd refresh` prints the package cache update command, eg.: `apt-get update`
* `installcmd refresh` prints the non-interactive install command, eg.: `apt-get install --assume-yes`
* `installcmd pkgspec foo.yml` prints the correct name of the package for that platform, based on information in the `foo.yml`.

Installcmd just prints the command, but it's easy to make your shell execute it:
 ```
# Without spec
$ $(installcmd) package-name

# With spec
$ $(installcmd pkgspec docker.yaml)
```

It's not magic. It searches through a built-in list of commands for various platforms (see [contribution guide](doc/contributing.md)). The package name specs have to be provided by you (see [package specs](doc/pkgspec.md)).

The main use of this is writing portable installation scripts, such as in your dotfiles repo or Dockerfiles. You can let installcmd handle the platform detection logic instead of having to reimplement it again and again, which makes the scripts a lot cleaner.
