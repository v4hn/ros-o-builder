#!/usr/bin/bash

docker build -t ros-one-jammy "$@" .
exec docker run -it ros-one-jammy:latest bash -l
