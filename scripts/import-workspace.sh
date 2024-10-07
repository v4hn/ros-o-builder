#!/usr/bin/bash

WORKSPACE=workspace
mkdir $WORKSPACE 2>/dev/null && echo "creating new folder '$WORKSPACE'" || echo "using existing folder '$WORKSPACE'"

if [[ -n "$1" ]]; then
  REPOS="$@"
else
  REPOS=sources.repos
fi

for f in $REPOS; do
  echo importing $f
  vcs import --shallow --recursive $WORKSPACE --input "$f" >/dev/null
done
