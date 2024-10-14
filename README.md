# A ROS-O deb repository for sid-one-unstable

## Github Preview Notice

If you are viewing this page on github.com, please note that the README.md preview on the repository page is incomplete.
Please view [the  file directly](https://github.com/v4hn/ros-o-builder/blob/sid-one-unstable/README.md) to see the full content.

## Install Instructions

```bash
echo "deb [trusted=yes] https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ ./" | sudo tee /etc/apt/sources.list.d/v4hn_ros-o-builder-sid-one-unstable.list
sudo apt update
sudo apt install python3-rosdep2
echo "yaml https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/local.yaml debian" | sudo tee /etc/ros/rosdep/sources.list.d/1-v4hn_ros-o-builder-sid-one-unstable.list
rosdep update

# install required packages, e.g.,
sudo apt install ros-one-desktop-full ros-one-plotjuggler ros-one-navigation [...]
```

## Build

|     |     |
| --- | --- |
| Target Distribution | sid-one |
| Architecture |  |
| Available Packages | 0 |
| Build Date | Mon Oct 14 12:04:02 UTC 2024 |

## Build Status

|   | Logs | Package | Version | Files | Upstream |
| - | ---- | ------- | ------- | ----- | -------- |
| <a id="[ros_environment](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros-one-ros-environment_1.3.2-5-g2686e94-2024.10.14.11.32_amd64.deb)" href="#[ros_environment](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros-one-ros-environment_1.3.2-5-g2686e94-2024.10.14.11.32_amd64.deb)">:green_circle:</a> | [:green_book:](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros_environment_1.3.2-5-g2686e94-2024.10.14.11.32-bloom_generate.log) [:green_book:](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros-one-ros-environment_1.3.2-5-g2686e94-2024.10.14.11.32_amd64-2024-10-14T11:32:41Z.build) | [ros_environment](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros-one-ros-environment_1.3.2-5-g2686e94-2024.10.14.11.32_amd64.deb) | 1.3.2-5-g2686e94-2024.10.14.11.32 | [:books:](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros-one-ros-environment_1.3.2-5-g2686e94-2024.10.14.11.32_amd64.files) | [:link:](https://github.com/ros-o/ros_environment/tree/debian) |
| <a id="[setup_files](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros-one-setup-files_0-2024.10.14.11.32_amd64.deb)" href="#[setup_files](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros-one-setup-files_0-2024.10.14.11.32_amd64.deb)">:green_circle:</a> | [:green_book:](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/setup_files_0-2024.10.14.11.32-bloom_generate.log) [:green_book:](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros-one-setup-files_0-2024.10.14.11.32_amd64-2024-10-14T11:32:10Z.build) | [setup_files](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros-one-setup-files_0-2024.10.14.11.32_amd64.deb) | 0-2024.10.14.11.32 | [:books:](https://raw.githubusercontent.com/v4hn/ros-o-builder/sid-one-unstable/repository/ros-one-setup-files_0-2024.10.14.11.32_amd64.files) | [:link:](https://github.com/v4hn/setup_files/tree/main) |

## Top Offenders (broken packages)

|   | Logs | Package | Version | Files | Upstream |
| - | ---- | ------- | ------- | ----- | -------- |
