#! /usr/bin/env python3

from .observation import isiterable

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
    assert isiterable(obj)
    it = iter(obj)
    curr = next(it)
    for head in it:
        yield (*curr, False) if isinstance(curr, tuple) else (curr, False)
        curr = head
    yield (*curr, False) if isinstance(curr, tuple) else (curr, False)
