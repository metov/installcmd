# Contribution guide
At a high level, installcmd has two components:

* An index of which command to use for which platform
* Logic for detecting the current platform and searching the index

Both are subject to diminishing returns.

There's some obvious functionality like compatibility with `apt-get` or `pacman` for example. This is low hanging fruit and straightforward to implement even for a single developer working in his free time. Such functionality is slated for completion by version 1.0.

There are **a lot** of platforms, package managers and packages out there. The only realistic way of attacking the problem is through a collaborative effort.

* If you discover a platform, OS or distro that installcmd detects incorrectly, please [create an issue](https://github.com/metov/installcmd/issues/new). Include some testing/reproduction steps so that a patch can be developed.
* If you come across a situation where the platform is detected correctly, but installcmd doesn't know the right package manager command, you can add the command to the [`commands.yaml` file](../installcmd/commands.yaml). The syntax should be pretty obvious. Fork the repo, make your changes, and submit a PR. Include some output from installcmd with the `--log DEBUG` argument.
* Individual package spec are mostly left to the users, but you can share them by submitting a PR that adds specs to [`pkgspec/`](../pkgspec). See also [package specs](src/pkgspec.md). The scalable solution to the package problem would be to write an automated matcher which generates the specs, but that is currently outside the scope of installcmd.

The vision for installcmd is that it will eventually support almost every platform and most commonly used packages. Handling every single corner case is likely not feasible, nor desirable: As we get into more and more obscure platforms, there's a point where the effort of supporting them is not worth the gain.
