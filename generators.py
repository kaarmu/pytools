#! /usr/bin/env python3

def warnLast(obj):
    """
    Generate, for iterables, a warning if you are at the last element.

    Much like enumerate, warnLast provides a second output. The second output
    is true if iterable is on last element.

    Example
    -------
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

def meld(*iterables):
    """
    Meld iterables to a single iterable with left-most argument priority.

    Similar to zip, meld modifies given iterables. The output is given by the
    most prioritized iterable and when that is empty, continues onto the next.
    The priority is increased the farther left the iterable is.

    Example
    -------
        iterable 0: 'abcd'
        iterable 1: 'efghi'
        iterable 2: 'jkl'
        iterable 3: 'mnopqrs'

        output: 'abcdirs'
    """
    for N, elms in enumerate(zip(*iterables)):
        yield elms[0]
    N += 1 # Max common length
    if iterables := [it[N:] for it in iterables if N < len(it)]:
        yield from meld(*iterables)

