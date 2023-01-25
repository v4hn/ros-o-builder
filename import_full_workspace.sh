#!/usr/bin/sh

mkdir ws 2>/dev/null && echo "creating new folder 'ws'" || echo "using existing folder 'ws'"

for f in *\.repos; do
  echo importing $f
  vcs import ws <$f >/dev/null
done
