#!/bin/bash

# current folder
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PDIR="$(dirname "$DIR")"

exec docker run -it --mount type=bind,source=$PDIR,destination=/ros-o-builder sid-ros-one:latest bash -l
