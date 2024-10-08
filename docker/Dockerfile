# unstable ubuntu-jammy docker with (some) preinstalled ros-one packages
FROM ubuntu:jammy

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt install -y vim less ca-certificates sudo bash-completion python3-pip git tmux python-is-python3
RUN apt install -y python3-bloom
RUN pip3 install catkin-tools

RUN echo "deb [trusted=yes] https://raw.githubusercontent.com/v4hn/ros-o-builder/jammy-one-unstable/repository ./" | sudo tee /etc/apt/sources.list.d/v4hn_ros-o-builder.list
RUN sudo apt update
RUN sudo apt install -y python3-rosdep2
RUN echo "yaml https://raw.githubusercontent.com/v4hn/ros-o-builder/jammy-one-unstable/repository/local.yaml debian" | sudo tee /etc/ros/rosdep/sources.list.d/1-v4hn_ros-o-builder.list
RUN rosdep update

RUN apt install -y ros-one-desktop-full
RUN echo "source /opt/ros/one/setup.bash" | tee -a /root/.bashrc
