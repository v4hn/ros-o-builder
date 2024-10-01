#!/usr/bin/bash

# Download logs for a specific GitHub Actions run
# Run in builder git repository
# Requires configured `gh` command line tool and `jq`

REPO=`git remote get-url origin | sed 's@https://github.com/@@'`
RUN_ID=$1

if [[ -z "$RUN_ID" ]]; then
  gh api repos/$REPO/actions/runs | python -m json.tool | jq '.workflow_runs[] | (.updated_at + " " + .name + " " + (.id|tostring))' | tac
  cat <<EOF
---
Usage:
  $0
    - list known workflow runs
  $0 <run_id>
    - download logs for a specific run (last column in list above)
EOF
else
  set -x
  gh api repos/$REPO/actions/runs/$RUN_ID/logs > logs.zip &&
  rm -rf logs &&
  mkdir logs &&
  unzip logs.zip -d logs >/dev/null
  set +x
fi

