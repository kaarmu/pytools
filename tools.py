#! /usr/bin/env python3
"""
Provide with a set of tools.

Includes:
    wait - sleep function
    iterable - checks if object is iterable
    warnLast - generator for iterables, warns if last element in iterable.
    Bin - Binary tools for unsigned manipulation.
"""

from time import time


def wait(t):
    """
    Wait until time has passed.

    Functionally the same as time.sleep, but more accurate since it doesn't
    rely on OS scheduler.
    """
    started = time()
    while time() - started < t:
        continue








