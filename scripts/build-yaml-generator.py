#!/usr/bin/env python

# Generate a YAML file for a GitHub Actions workflow to implement a staged build of ROS packages.
# This only ever needs to be run when changes need to be made to the build workflow.
# It is NOT invoked during the regular build process.
# Legit reasons to run this script are:
# - to change the number of build stages if longer dependency chains are introduced
# - change the number of workers per stage
# - include other changes to the build workflow in the script itself and regenerate the YAML file accordingly

import em

# Stages are defined by dependency levels.
# Each stage builds packages that depend only on packages from previous stages.
# This needs to be >= the maximum dependency level in the package set.
NR_OF_STAGES = 19

# GHA allows up to 20 parallel jobs per free account (not repository)
# The number of actually active workers per stage is further reduced by job assignment,
# so this specifies an upper limit.
MAXIMUM_NR_OF_WORKERS_PER_STAGE = 10

###

BUILD_YAML_TEMPLATE = R"""name: build

on:
  workflow_dispatch:
  schedule:
    # build weekly to find breakage
    - cron: '13 1 * * 6'

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}

env:
  DISTRIBUTION: ubuntu
  DEB_DISTRO: jammy
  BRANCH: jammy-one-experimental
  JOBS_YAML: /home/runner/jobs.yaml
  AGG: /home/runner/apt_repo_dependencies

jobs:
  stage-1:
    runs-on: ubuntu-24.04
    outputs:
      workers: ${{ steps.prepare.outputs.workers }}
    steps:
      - name: Check out the repo
        uses: actions/checkout@@v4
      - name: Prepare Pipeline
        id: prepare
        uses: ./.github/actions/prepare-worker-pipeline
      - name: rosdep keys
        shell: bash
        run: |
          cat ${{ env.AGG }}/local.yaml
      - name: jobs
        shell: bash
        run: |
          cat ${{ env.JOBS_YAML }}
@[for i, workers in stages]@[for j in range(workers)]
  stage@i-worker@j:
    uses: ./.github/workflows/worker.yaml
    if: (always() && !cancelled()) && contains( needs.stage-1.outputs.workers, 'stage@i-worker@j' )
    needs: stage@(i-1)
    with:
      worker: stage@i-worker@j
      depends: stage@(i-1)@[end for]
  stage@i:
    uses: ./.github/workflows/aggregate-debs.yaml
    if: always() && !cancelled()
    needs: [@[for j in range(workers)]stage@(i)-worker@j, @[end for]]
    with:
      stage: @i
@[end for]
  deploy:
    needs: stage@last_stage
    if: always() && !cancelled()
    runs-on: ubuntu-24.04
    steps:
      - name: get apt packages from last job
        uses: actions/cache/restore@@v4
        with:
          path: ${{ env.AGG }}
          key: apt-repo-stage@last_stage-${{ github.sha }}-${{ github.run_id }}-${{ github.run_attempt }}
          restore-keys: |
            apt-repo-stage@last_stage-${{ github.sha }}-${{ github.run_id }}
      - name: move packages to repo
        run: |
          mv ${{ env.AGG }} /home/runner/apt_repo
      - uses: v4hn/ros-deb-builder-action/deploy@@roso-noble
        with:
          BRANCH: ${{ env.BRANCH }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SQUASH_HISTORY: true
"""

if __name__ == '__main__':
    first_stage = [1] # the first stage only builds two tiny support packages
    workers = first_stage + [10] * (NR_OF_STAGES - len(first_stage))

    print(em.expand(BUILD_YAML_TEMPLATE, stages=enumerate(workers), last_stage=NR_OF_STAGES-1), end='')
