#!/bin/sh

distro=
stable=

usage() {
   echo "Usage: $0 [distro] [-r previous_distro]" >&2
   exit 1
}

PARSED=$(getopt -o r:h -n "$0" -- "$@") || usage
eval set -- "$PARSED"
while true; do
   case "$1" in
      -r) stable="$2"; shift 2 ;;
      -h) usage ;;
      --) shift; break ;;
      *) usage ;;
   esac
done

distro=$1
if [ -z "$distro" ]; then
   usage
fi

URL=https://raw.githubusercontent.com/v4hn/ros-o-builder/refs/heads

# csv header is
# Package,Version,URL,Status,Bloom Log,Build Log,Deb File,Installed Files

if [ -z "$stable" ]; then
   curl -s "$URL/$distro/pkg_build_status.csv" | tail -n+2 | awk -F, -v repo="$URL/$distro/repository" '
   $4 != "success" {
       if($4 == "failed-bloom-generate"){
            report=$5;
       } else {
            report=$6;
       }
       print("Package: " $1 "\nLog: " repo "/" report "\nUpstream: " $3 "\n---")
   }
   '
   exit 0
fi

tmp_prev=$(mktemp) || exit 1
tmp_cur=$(mktemp) || { rm -f "$tmp_prev"; exit 1; }
trap 'rm -f "$tmp_prev" "$tmp_cur"' EXIT

curl -s "$URL/$prev/pkg_build_status.csv" > "$tmp_prev" || exit 1
curl -s "$URL/$distro/pkg_build_status.csv" > "$tmp_cur" || exit 1

awk -F, -v repo="$URL/$distro/repository" '
# first file (previous): build map package -> status
NR==FNR {
   if (FNR==1) next;  # skip header
   prev_status[$1]=$4;
   next;
}

# second file (current): skip header, show only regressions (failed now, succeeded before)
FNR==1 { next; }
$4 != "success" && prev_status[$1] == "success" {
   if($4 == "failed-bloom-generate"){
      report=$5;
   } else {
      report=$6;
   }
   print("Package: " $1 "\nLog: " repo "/" report "\nUpstream: " $3 "\n---")
}
' "$tmp_prev" "$tmp_cur"
