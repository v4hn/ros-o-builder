#!/usr/bin/bash

mkdir ws 2>/dev/null && echo "creating new folder 'ws'" || echo "using existing folder 'ws'"

if [[ -n "$1" ]]; then
  REPOS="$@"
else
  eval REPOS=*\.repos
fi

for f in $REPOS; do
  echo importing $f
  vcs import --shallow --recursive ws <$f >/dev/null
done
