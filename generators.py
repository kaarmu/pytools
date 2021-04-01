#! /usr/bin/env python3

from random import choice
from time import sleep
from math import cos, inf, pi
from functools import reduce


#
# Sources
#

def inflist(start=0, stop=inf, step=1):
    op = (lambda x, y: x < y) if step > 0 else (lambda x, y: x > y)
    while op(start, stop):
        yield start
        start += step

def birth(N, population=[0,1]):
    """ From a population, generate a sample randomly. """
    for _ in range(N):
        yield choice(population)

def randColors(N=1):
    hexabet = '123456789ABCDEF'
    for _ in range(N):
        yield '#' + ''.join(birth(6, hexabet))

def loop(iterable):
    while True:
        yield from iterable

#
# Modifiers
#

def sleepy(iterable, T=0.5):
    """
    Cause a generator to be sleepy.

    A very simple generator that yields values only after T seconds.
    """
    for elm in iterable:
        sleep(T)
        yield elm

def periodic(iterable, period=4):
    """
    Return a periodic value of the index.

    Fun example
    -----------
    >>> for x, _ in periodic(inflist(), 128):
    ...     sleep(0.25 * abs(x))
    ...     print('x', end='', flush=True)

    """
    for i, elm in enumerate(iterable):
        x = cos((i % period)*pi/period)
        yield x, elm

def printer(iterable):
    """
    The simplest printer genereator ever.
    """
    for elm in iterable:
        print(elm)
        yield elm

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

#
# Channels
#

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
    N = 0 # Max common length
    for elms in zip(*gs):
        N += 1
        yield elms[0]
    if gs := [it[N:] for it in gs if N < len(it)]:
        yield from meld(*gw)

def mux(*gs, func=None):
    """
    Fun Example
    -----------
    >>> for ch in mux(inflist(), 'a'*20, 'b'*20, func=lambda els: els[1 + els[0] % 2]):
    ...     print(ch)
    """
    func = func or truthy
    yield from (func(els) for els in zip(*gs))

#
# Sinks
#

def truthy(it):
    """
    Prioritizes first element which is truthy.
    """
    if it[0]:
        return it[0]
    if el := truthy(it[1:]):
        return el
    return it[0]



def sink(it):
    for _ in it:
        pass

