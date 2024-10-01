#!/usr/bin/bash

mkdir workspace 2>/dev/null && echo "creating new folder 'ws'" || echo "using existing folder 'ws'"

if [[ -n "$1" ]]; then
  REPOS="$@"
else
  REPOS=sources.repos
fi

for f in $REPOS; do
  echo importing $f
  vcs import --shallow --recursive workspace --input "$f" >/dev/null
done
