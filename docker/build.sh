#!/usr/bin/bash

# optionally pass --no-cache
docker build -t ros-one-jammy "$@" .

exec docker run -it ros-one-jammy:latest bash -l
