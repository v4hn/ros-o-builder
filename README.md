# ros-o-builder - Building deb packages for ROS-O.

THIS IS AN EXPERIMENTAL REPOSITORY. DO NOT RELY ON IT (yet).

This repository aims to build the extended ROS ecosystem for Debian-based distributions in `ros-one-*.deb` packages on github's CI system.

At the moment the only target platform is Ubuntu 22.04, but this is likely to change in the future.

See [the install directives](https://github.com/v4hn/ros-o-builder/blob/jammy-one/README.md) for how to test it on your system.

See the [ros-o-overlay example repo](https://github.com/v4hn/ros-o-overlay) for how to set up an overlay to build additional packages based on the ones from here.

Alternatively [a trivial docker Dockerfile is available](https://github.com/v4hn/ros-o-builder/tree/main/docker) to test the installation.
