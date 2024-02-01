```bash
echo "deb [trusted=yes] https://raw.githubusercontent.com/v4hn/ros-o-builder/jammy-one/ ./" | sudo tee /etc/apt/sources.list.d/v4hn_ros-o-builder-jammy-one.list
sudo apt update
sudo apt install python3-rosdep2
echo "yaml https://raw.githubusercontent.com/v4hn/ros-o-builder/jammy-one/local.yaml debian" | sudo tee /etc/ros/rosdep/sources.list.d/1-v4hn_ros-o-builder-jammy-one.list
rosdep update
```
