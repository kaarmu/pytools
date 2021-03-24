#! /usr/bin/env python3

from random import choice

def warnLast(obj):
    """
    Generate, for iterables, a warning if you are at the last element.

    Much like enumerate, warnLast provides a second output. The second output
    is true if iterable is on last element.

    [] -> [curr] -> [head] -> []
    return curr, False

    [] -> [] -> [curr] -> [head]
    return curr, False

    [] -> [] -> [] -> [curr]
    return curr, True
    """
    it = iter(obj)
    curr = next(it)
    for head in it:
        yield (*curr, False) if isinstance(curr, tuple) else (curr, False)
        curr = head
    yield (*curr, True) if isinstance(curr, tuple) else (curr, True)

def birth(N, population=[0,1]):
    for _ in range(N):
        yield choice(population)
