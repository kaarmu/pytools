#! /usr/bin/env python3

from random import choice
from time import sleep
from math import cos, inf, pi
from functools import reduce
from itertools import tee

from itertools import *

#
# Sources
#

# itertools.count  ~ inflist
# itertools.cycle
# itertools.repeat ~ loop

def birth(N, population=[0,1]):
    """ From a population, generate a sample randomly. """
    for _ in range(N):
        yield choice(population)

def randAlph(N=1):
    alphabet = 'abcdefghjklmnopqrstuwvxyz'
    yield from birth(N, alphabet)

def randColors(N=1):
    hexabet = '123456789ABCDEF'
    for _ in range(N):
        yield '#' + ''.join(birth(6, hexabet))

#
# Modifiers
#

# itertools.accumulate
# itertools.starmap

def sleepy(it, T=0.5):
    """
    Cause a generator to be sleepy.

    A very simple generator that yields values only after T seconds.
    """
    for el in it:
        sleep(T)
        yield el

def periodic(it, period=4):
    """
    Return a periodic value of the index.

    Fun example
    -----------
    >>> for x, _ in periodic(inflist(), 128):
    ...     sleep(0.25 * abs(x))
    ...     print('x', end='', flush=True)

    """
    for i, elm in enumerate(it):
        x = cos((i % period)*pi/period)
        yield x, elm

def printer(it):
    """
    The simplest printer genereator ever.
    """
    for elm in it:
        print(elm)
        yield elm

def expand(it, n):
    """
    Expand the first n values.

    Use this generator to, e.g. look ahead on the values to come.

    Example
    -------
    >>> for i, j, none* in expand(range(4), 2):
    ...     print(i,j)
    0 1
    1 2
    2 3
    >>> for i,j,k,*l in expand('abcdefg', 3):
    ...     print(i,j,k,l)
    a b c ['d', 'e', 'f', 'g']
    b c d ['e', 'f', 'g']
    c d e ['f', 'g']
    d e f ['g']
    e f g []


    """
    while len(expd := it[:n]) == n:
        yield expd
        it = it[1:]

def warnLast(obj):
    """
    Generate, for its, a warning if you are at the last element.

    Much like enumerate, warnLast provides a second output. The second output
    is true if it is on last element.

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

#
# Channels
#

# itertools.chain
# itertools.compress
# itertools.dropwhile
# itertools.filterfalse
# itertools.islice
# itertools.takewhile
# itertools.tee
# itertools.zip_longest
# itertools.product
# itertools.permutations
# itertools.combinations


def pipe(*gs):
    """
    Take multiple (uninitialized) generators and pipe them together.

    First argument is original generator and source. Thus best if
    initialized by user.

    Example
    -------
        piper(f(...), g, h) -> h(g(f(...)))

        Think of this like,
        f(...) | g | h | ...
    """
    gs, last = gs[:-1], gs[-1]
    yield from last(pipe(*gs)) if gs else last

def purepipe(*gs):
    """
    Much like pipe but doesn't expect a source in the beginning.

    Returns an uninitialized generator function p(g) where g would
    be its source generator.

    Example
    -------
        p = purepipe(f1, f2)
        p(g(...)) -> f2(f1(g(...)))
    """
    return lambda g: (yield from pipe(g, *gs))

def meld(*gs):
    """
    Meld its to a single it with left-most argument priority.

    Similar to zip, meld modifies given its. The output is given by the
    most prioritized it and when that is empty, continues onto the next.
    The priority is increased the farther left the it is.

    Example
    -------
        it 0: 'abcd'
        it 1: 'efghi'
        it 2: 'jkl'
        it 3: 'mnopqrs'

        output: 'abcdirs'
    """
    N = 0 # Max common length
    for els in zip(*gs):
        N += 1
        yield els[0]
    if gs := [it[N:] for it in gs if N < len(it)]:
        yield from meld(*gw)

#
# Sinks
#

def sink(it):
    for _ in it:
        pass

def truthy(it):
    """
    Prioritizes first element which is truthy.
    """
    if it[0]:
        return it[0]
    if el := truthy(it[1:]):
        return el
    return it[0]


