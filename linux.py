#! /usr/bin/env python3

import shutil
import subprocess

PATHS = {}

def _callWhichAndCache(name: str) -> str:
    path =  shutil.which(name)
    assert path is not None, f'"{name}" cannot be found'
    PATHS[name] = path
    return path

def _find(name: str) -> str:
    return PATHS[name] if name in PATHS else _callWhichAndCache(name)

def modprobe(*args, sudo=False):
    cmd = [_find('modprobe'), *args]
    if sudo:
        cmd = [_find('sudo'), *cmd]
    return subprocess.run(cmd)

def lsof(*args, sudo=False):
    cmd = [_find('lsof'), *args]
    if sudo:
        cmd = [_find('sudo'), *cmd]
    return subprocess.run(cmd)

