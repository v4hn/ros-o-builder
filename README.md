# A ROS-O deb repository for bookworm-one-unstable

## Github Preview Notice

If you are viewing this page on github.com, please note that the README.md preview on the repository page is incomplete.
Please view [the `README.md` file directly](https://github.com/v4hn/ros-o-builder/blob/bookworm-one-unstable/README.md) to see the full content.

## Install Instructions

```bash
echo "deb [trusted=yes] https://raw.githubusercontent.com/v4hn/ros-o-builder/bookworm-one-unstable/repository/ ./" | sudo tee /etc/apt/sources.list.d/v4hn_ros-o-builder-bookworm-one-unstable.list
sudo apt update
sudo apt install python3-rosdep2
echo "yaml https://raw.githubusercontent.com/v4hn/ros-o-builder/bookworm-one-unstable/repository/local.yaml debian" | sudo tee /etc/ros/rosdep/sources.list.d/1-v4hn_ros-o-builder-bookworm-one-unstable.list
rosdep update

# install required packages, e.g.,
sudo apt install ros-one-desktop-full ros-one-plotjuggler ros-one-navigation [...]
```

## Build

|     |     |
| --- | --- |
| Target Distribution | bookworm-one |
| Architecture |  |
| Available Packages | 0 |
| Build Date | Sat Nov 28 09:01:34 UTC 2026 |
