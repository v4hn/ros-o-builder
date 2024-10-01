# ros-o-builder - Your Own Online Builder for ROS-O deb Packages

This repository builds an extended ROS ecosystem for Debian-based distributions in `ros-one-*.deb` packages on GitHub's free GitHub Action.

**Target Distribution**: At the moment packages are build for Ubuntu 22.04 jammy - other Debian-based target distributions can be setup as well.

**Build Time**: Build times vary on the amount of packages selected. An extended system of around 850 packages takes around 12 hours to build using the staged parallel builder.

## Usage

You can either [rely on this repository](https://github.com/v4hn/ros-o-builder/blob/jammy-one/README.md#install-instructions), or fork it to control package versions and syncs yourself.

### Setup instructions for your own fork

**Step 1:** Fork this repository.

**Step 2:** Adjust Permissions.
To use this repository yourself, you need [to change github's default permissions](https://github.com/ad-m/github-push-action/?tab=readme-ov-file#requirements-and-prerequisites) for the actions of your forked repository.

**Step 3 [optional]:** Navigate to Settings -> Pages -> Deploy from a branch and select the `<distro>-one` or `<distro>-one-unstable` branch to deploy a clean github page based on the generated `README.md`.

## Branch Overview

- `main` contains the [github workflow configurations](https://github.com/v4hn/ros-o-builder/tree/main/.github) and the [sources.repos](https://github.com/v4hn/ros-o-builder/blob/main/sources.repos) file.

- `<distro>-one-unstable` contains the generated results of each individual action run (either manually triggered or scheduled)

- `<distro>-one` contains a snapshot of `<distro>-one-unstable` that can be updated (or *synced*) by the user using the provided `sync-unstable` action workflow with the respective `<distro>-one-unstable` branch.

## How to Add Packages

[`sources.repos`](https://github.com/v4hn/ros-o-builder/tree/main/sources.repos) contains the list of repositories to build.
To add additional packages, you simply need to add new entries to this file. Still, to avoid problems during integration, it is recommended to follow these steps:

**Step 1:** Setup a [ros-o-overlay](https://github.com/v4hn/ros-o-overlay) fork and build the packages there.

**Step 2:** Fix potential build issues in the overlay (as package builds in the main builder take much longer).

**Step 3:** Propose a pull-request to add the `sources.repos` entries in this repository (or your fork). Notice that this is *not* a fully-featured buildfarm and we might exclude your packages for build time reasons.

## Compatibility with OpenRobotics' ROS2 packages

The packages built here rely on Debian packages of ROS core infrastructure [[0](https://packages.debian.org/source/sid/ros-rosdep), [1](https://packages.debian.org/source/sid/ros-catkin)]. For multiple reasons -partly technical, partly political- these packages are not compatible with OpenRobotics' ROS2 packages which build very similar packages themselves in incompatible ways. It is possible to set up a very similar builder based on individual OpenRobotics' deb repositories though.

## TODOs

### Explicitly Planned Packages to Add

- https://github.com/cra-ros-pkg/robot_localization
- https://github.com/locusrobotics/fuse
- https://github.com/avidbots/flatland
- http://wiki.ros.org/stdr_simulator ([issue](https://github.com/stdr-simulator-ros-pkg/stdr_simulator/issues/210))
- https://github.com/cartographer-project/cartographer_ros ([issue](https://github.com/cartographer-project/cartographer_ros/issues/1766))

- https://github.com/loco-3d/crocoddyl
- https://github.com/tesseract-robotics
- https://github.com/stack-of-tasks
- https://github.com/ipab-slmc/exotica

- https://github.com/frankaemika/franka_ros
- https://github.com/UniversalRobots/Universal_Robots_ROS_Driver
- https://github.com/TAMS-Group/robotiq
- https://github.com/hanruihua/Turtlebot2_on_Noetic

### Target Platforms

- Debian sid
- Ubuntu noble

### Internals

- record build times 
  - use them in task-to-worker assignment

- ensure sources.repos contains at most N stages (as provided by the build.yaml)

- constraint solver for graph partitioning by packages/build times
  - likely still map to the same staged workers for predictable GH caching

- reduce network load by caching debs
  - set up https://launchpad.net/squid-deb-proxy
  - or investigate whether a development version of deb-cacher-ng resolves sporadic 503 errors
