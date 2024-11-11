#!/bin/sh

distro=$1
if [ -z "$distro" ]; then
   distro=jammy
fi

REPO=https://raw.githubusercontent.com/v4hn/ros-o-builder/refs/heads/$distro-one-unstable

# csv header is
# Package,Version,URL,Status,Bloom Log,Build Log,Deb File,Installed Files

curl -s $REPO/pkg_build_status.csv | tail -n+2 | awk -F, -v repo=$REPO/repository '
$4 != "success" {
   if($4 == "failed-bloom-generate"){
      report=$5;
   } else {
      report=$6;
   }
   print("Package: " $1 "\nLog: " repo "/" report "\nUpstream: " $3 "\n---")
}
'
