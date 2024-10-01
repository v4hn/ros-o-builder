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
  AGG: /home/runner/apt_repo_dependencies
  DISTRIBUTION: ubuntu

jobs:
  stage-1:
    runs-on: ubuntu-24.04
    outputs:
      workers: ${{ steps.worker.outputs.workers }}
    env:
      JOBS_YAML: /home/runner/jobs.yaml
    steps:
      - name: Check out the repo
        uses: actions/checkout@@v4
      - name: Clone sources
        run: |
          echo 'Acquire::Retries "20";'                  | sudo tee -a /etc/apt/apt.conf.d/80-retries
          echo 'Acquire::Retries::Delay::Maximum "300";' | sudo tee -a /etc/apt/apt.conf.d/80-retries
          echo 'Debug::Acquire::Retries "true";'         | sudo tee -a /etc/apt/apt.conf.d/80-retries
          sudo add-apt-repository -y ppa:v-launchpad-jochen-sprickerhof-de/ros
          sudo apt update
          DEBIAN_FRONTEND=noninteractive sudo apt install -y vcstool catkin
          mkdir workspace
          vcs import -w 5 --recursive --shallow --input sources.repos workspace
      - name: Prepare rosdep keys
        run: |
          cp rosdep.yaml local.yaml
          echo >> local.yaml # ensure trailing newline
          for PKG in $(catkin_topological_order --only-names workspace); do
            printf "%s:\n  %s:\n  - %s\n" "$PKG" "${{ env.DISTRIBUTION }}" "ros-one-$(printf '%s' "$PKG" | tr '_' '-')" | tee -a local.yaml
          done
      - name: Prepare Jobs
        id: worker
        run: |
          ./scripts/generate-jobs.py workspace | tee ${{ env.JOBS_YAML }}
          echo "workers=$(cat ${{ env.JOBS_YAML }} | sed -n '/^stage.*:$/ p' | tr -d '\n')" >> $GITHUB_OUTPUT
      - name: Store jobs cache
        uses: actions/cache/save@@v4
        with:
          path: ${{ env.JOBS_YAML }}
          key: jobs-${{ github.sha }}-${{ github.run_id }}-${{ github.run_attempt }}
      - name: Prepare meta data cache
        run: |
          mkdir -p ${{ env.AGG }}
          mv local.yaml ${{ env.AGG }}/local.yaml
          cp sources.repos ${{ env.AGG }}/sources_specified.repos
          mkdir -p ${{ env.AGG }}/.github/workflows
          cp .github/workflows/sync-unstable.yaml ${{ env.AGG }}/.github/workflows/sync-unstable.yaml
      - name: Store meta data cache
        uses: actions/cache/save@@v4
        with:
          path: ${{ env.AGG }}
          key: apt-repo-stage-1-${{ github.sha }}-${{ github.run_id }}-${{ github.run_attempt }}
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
    env:
      ROS_DISTRO: one
      DEB_DISTRO: jammy
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
          BRANCH: ${{ env.DEB_DISTRO }}-${{ env.ROS_DISTRO }}-unstable
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SQUASH_HISTORY: true
"""

if __name__ == '__main__':
    first_stage = [1] # the first stage only builds two tiny support packages
    workers = first_stage + [10] * (NR_OF_STAGES - len(first_stage))
    
    print(em.expand(BUILD_YAML_TEMPLATE, stages=enumerate(workers), last_stage=NR_OF_STAGES-1), end='')
