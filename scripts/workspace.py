#!/usr/bin/env python
# authored 2023 by Michael 'v4hn' Goerner

import catkin_pkg.packages
import sys
import os
import subprocess
import cmd
from collections import namedtuple
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Set, List, NamedTuple

def get_repository(path):
    '''
    returns path to root of git repository containing path
    '''
    p = path
    while not (p / '.git').is_dir() and p != p.parent:
        p = p.parent
    if p == p.parent:
        raise Exception(f"{path} is not inside a git repository")
    return p.as_posix()

def get_git_info(path):
    def call(cmd):
        return subprocess.run(
            cmd.split(" "),
            stdout=subprocess.PIPE,
            cwd=path,
            text=True
            ).stdout.strip()
    version = call('git symbolic-ref --short HEAD')
    long_ref = call('git symbolic-ref -q HEAD')
    remote = call(f'git for-each-ref --format=%(upstream:remotename) {long_ref}')
    url = call(f'git remote get-url {remote}')
    if not remote:
        print(f"ERROR: no remote found for {path}")
    return url, version

@dataclass
class Package:
    name: str
    path: str
    repository: str
    # these are packages
    build_depends: Set[str]
    exec_depends: Set[str]
    test_depends: Set[str]

@dataclass
class Repository:
    name: str
    path: str
    packages: Set[Package]

    # these are repositories
    build_depends: Set[str]
    exec_depends: Set[str]
    test_depends: Set[str]

    # these are repositories with cyclic build/test dependencies
    # such dependencies are not allowed by ROS on the package graph, but can arise in the repository groups
    # THEY ARE EXPLICITLY EXCLUDED ABOVE
    bonded: Set[str] = None

class Workspace:
    '''
    Interface to structure repository and package dependencies in a catkin workspace
    '''

    @property
    def repositories(self):
        return self._repos

    @property
    def packages(self):
        return self._pkgs

    def __init__(self, ws):
        if ws.endswith('/'):
            ws = ws[:len(ws)-1]
        self.ws = Path(ws)
        self.cut_prefix = 0 if ws == "." else len(ws)+1

        # index of all packages in workspace
        self._pkgs = {
            catpkg['name']: Package(
                name=catpkg['name'],
                path=path,
                repository=get_repository(self.ws/path)[self.cut_prefix:],
                build_depends=set([d.name for d in catpkg['build_depends']]),
                exec_depends=set([d.name for d in catpkg['exec_depends']]),
                test_depends=set([d.name for d in catpkg['test_depends']]),
                )
            for (path, catpkg) in catkin_pkg.packages.find_packages(ws).items()
        }

        # index of all repositories in workspace
        self._repos= {}
        repository_names = set([p.repository for p in self._pkgs.values()])
        for name in repository_names:
            pkgs = [p for p in self._pkgs.values() if p.repository == name]
            self._repos[name] = Repository(
                name=name,
                path=repository_names,
                packages=[pkg for pkg in self._pkgs.values() if pkg.repository == name],
                build_depends=set([self._pkgs[d].repository for pkg in pkgs for d in pkg.build_depends if d in self._pkgs]).difference([name]),
                exec_depends=set([self._pkgs[d].repository for pkg in pkgs for d in pkg.exec_depends if d in self._pkgs]).difference([name]),
                test_depends=set([self._pkgs[d].repository for pkg in pkgs for d in pkg.test_depends if d in self._pkgs]).difference([name]),
                )

        # find cyclic build/test dependencies
        for repo in self._repos.values():
            while True:
                cycle = self.detect_cycle(repo)
                if not cycle:
                    break
                bonded = set(cycle)
                for cyc_repo in cycle:
                    cyc_repo_bonds = self._repos[cyc_repo].bonded
                    if cyc_repo_bonds:
                        bonded.update(cyc_repo_bonds)

                for cyc_repo in bonded:
                    self._repos[cyc_repo].bonded = bonded

                # drop the cyclic dependencies in build and test dependencies
                for cyc_repo in bonded:
                    self._repos[cyc_repo].build_depends.difference_update(bonded)
                    self._repos[cyc_repo].exec_depends.difference_update(bonded)
                    self._repos[cyc_repo].test_depends.difference_update(bonded)

    def detect_cycle(self, rep, visited= None):
        if visited is None:
            visited = []
        visited.append(rep.name)
        deps = rep.build_depends.union(rep.test_depends, rep.exec_depends)
        for d in deps:
            try:
                i = visited.index(d)
                # cycle found
                return set(visited[i:])
            except ValueError:
                pass
            if d in self._repos:
                cycle = self.detect_cycle(self._repos[d], visited)
                if cycle:
                    return cycle
        visited.pop()
        return set()

    def drop_repository(self, repository):
        for p in self._repos[repository].packages:
            del self._pkgs[p.name]
            # remove pkg from other pkg dependencies
            for p in self._pkgs.values():
                p.build_depends.difference_update([p.name])
                p.exec_depends.difference_update([p.name])
                p.test_depends.difference_update([p.name])

        del self._repos[repository]
        # remove repository from other repositories dependencies
        for r in self._repos.values():
            r.build_depends.difference_update([repository])
            r.exec_depends.difference_update([repository])
            r.test_depends.difference_update([repository])

if __name__ == '__main__':
    ws = Workspace(sys.argv[1] if len(sys.argv) > 1 else ".")
    print("digraph ros {")
    for r in ws.repositories.values():
        for d in r.build_depends:
            print(f"{r.name} -> {d};")
    print("}")
