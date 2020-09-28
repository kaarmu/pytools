#! /usr/bin/env python3

from functools import reduce
import operator as op

from numbers import Integral
from collections.abc import MutableSequence

def ispower2(x):
    if x == 0:
        return -1
    elif x == 1:
        return 0
    elif x % 2:
        return -1
    else:
        return ispower2(x // 2) + 1 or -1

def ceilpow2(x):
    i = 1
    while 2**i < x:
        i += 1
    return i

def floorpow2(x):
    return ceilpow2(x) - 1

def unsignify(x, nbits=8):
    g_mask = 2**nbits - 1
    return (~x + 1)


class Converter:
    
    @staticmethod
    def EncodeHamming(nbitblock, data):
        """
        Encode data in hamming code for error bit recreation.

        If nbit = 16 bits -> create H(15, 11) with the first (from LSB) 11 bits.
        
        16 nbits -> 4 parity bits, 16-1-4 = 11 value bits
        32 nbits -> 6 parity bits, 32-1-6 = 25
        2^n nbits -> n parity bits, 2^n -1 -n  value bits
        """
        
        assert (nof_parity := ispower2(nbitblock)) != -1, 'Number of parity bits (size of bit-block) must be a power of 2.'
        nof_data = nbitblock - nof_parity - 1

        parity_bits = reduce(op.xor, BinT(nof_data).getWhereHigh(data))

class blis(Integral, MutableSequence):
    def __init__(self, arg1=None, arg2=None):
        """
        Create a binary list of either an integer or iterable bools.

        [True, True, False, True]
        1 1 0 1
        0b1101
        13        

        Arguments:
            - blis(value)
            - blis(value, nbits)
            - blis(iterable)
            - blis(iterable, nbits)
            Types:
                value - int
                iterable - [tuple, list]
                nbits - int
        """

        self.bits = []

        if (arg1 and arg2) is None:
            return

        typ = type(arg1)
        if typ is int:
            self.__from_value(arg1, arg2)

        elif typ in (list, tuple):
            self.__from_sequence(arg1, arg2)
        
        elif typ is type(self):
            self.bits = [elm for elm in arg1.bits]
            if arg2 is not None:
                self.bits = self.bits[:arg2] # if smaller nbits
                while len(self.bits) < arg2: # if larger nbits
                    self.bits.append(False)
        
        else:
            raise TypeError(f'Expected first argument to be either '
                            f'int, list, tuple or blis, not {typ}.')

    def __from_value(self, val, nbits=None):
        nbits = nbits or 8
        self.bits = list(BinT(nbits).represent(val))

    def __from_sequence(self, seq, nbits=None):
        nbits = nbits or max(len(seq), 8)
        self.bits = []
        for elm in seq:
            assert type(elm) is bool, (f'Expected elements of type '
                                       f'bool, not {type(elm)}')
            self.bits.append(elm)
        self.bits = self.bits[:nbits]

    def nbits(self):
        return len(self.bits)

    def __repr__(self):
        return ''.join(1 if val else 0 for val in reversed(self.bits))

    def __str__(self):
        return repr(self)

    def __abs__(self):
        return -self if self.bits[-1] else +self
    
    def __add__(self, other):
        if type(other) is not type(self):
            other = blis(other)
        nbits = max(self.nbits(), other.nbits())
        val = int(self) + int(other)
        return blis(val, nbits)

    def __and__(self, other):
        if type(other) is not type(self):
            other = blis(other)
        nbits = max(self.nbits(), other.nbits())
        val = BinT(nbits).andAt(int(self), int(other))
        return blis(val, nbits)
        # if other.nbits() > self.nbits():
        #     return NotImplemented # Make sure that self.nbits is greatest
        # nbits = self.nbits()
        # val = [elm for elm in self.bits]
        # val = [a and b for a, b in zip(val, other.bits)]
        # return blis(val, nbits)
        

    def __ceil__(self):
        pass

    def __delitem__(self, arg):
        pass

    def __eq__(self, other):
        pass

    def __floor__(self):
        pass

    def __floordiv__(self, other):
        pass

    def __getitem__(self, arg):
        pass

    def __int__(self):
        value = 0
        for i, bit in enumerate(self.bits):
            if bit:
                value += 1 << i
        if self.bits[-1]:
            value -= 2**len(self.bits)
        return value

    def __invert__(self):
        pass

    def __le__(self, other):
        pass

    def __len__(self):
        pass

    def __lshift__(self, arg):
        pass

    def __lt__(self, other):
        pass

    def __mod__(self, arg):
        pass

    def __mul__(self, other):
        pass

    def __neg__(self):
        pass

    def __or__(self, other):
        pass

    def __pos__(self):
        pass

    def __pow__(self, arg):
        pass

    def __radd__(self, other):
        pass

    def __rand__(self, other):
        pass

    def __rfloordiv__(self, other):
        pass

    def __rlshift__(self, arg):
        pass

    def __rmod__(self, arg):
        pass

    def __rmul__(self, other):
        pass

    def __ror__(self, other):
        pass

    def __round__(self, arg):
        pass

    def __rpow__(self, arg):
        pass

    def __rrshift__(self, arg):
        pass

    def __rshift__(self, arg):
        pass

    def __rtruediv__(self, other):
        pass

    def __rxor__(self, other):
        pass

    def __setitem__(self, arg1, arg2):
        pass

    def __truediv__(self, other):
        pass

    def __trunc__(self):
        pass

    def __xor__(self, other):
        pass

    def insert(self):
        pass


class BinT:
    """A collection of binary tools for unsigned ints."""

    def __init__(self, nbit, asup=True):
        """
        Construct Bin with a global_mask and settings.

        The constructor for Bin is not so much because it is an object,
        but rather to specify the number of bits and if one should use
        asuperior.

        The perhaps most important feature of Bin is that its operations
        will return an unsigned result, even if an operand is signed!
        However, be cautious if you use signed operands with this tool.

        g_mask: Global mask, will create a sequence of 1:s for all valid
        bits.

        senior: g_mask + 1 or also 1 << nbit. Will be one more bit than what is
        allowed.

        asuperior: a (is) superior, will apply to binary operations (a,b).
        When asuperior=False, a binary operation will operate a @ b and keep
        only bits il, all other bits are set to 0. One can say, it has a
        "background" of 0 and on bits il it have the result from a @ b.
        However, one could wish to keep the "background" of an operand.
        Therefore, asuperior=True exists, which states that a is the superior
        operand and thusly the "background" shall be a.
        (In the former, asuperior=False, there is no superior operand which
        makes the two "equal")
        This only applies to binary operations. In unary operations, a is
        always superior.
        # Ex.
        # asuperior=False: andNot(0b1011, 0b0101, 0) -> 0b001
        # asuperior=True: andNot(0b1011, 0b0101, 0) -> 0b1011
        # asuperior=True: andNot(0b1010, 0b0100, 0) -> 0b1010

        Bits are 0-indexed.
        It is possible to apply multiple indices in one call. This is done by
        argument expansion of il (index-list, though it is a tuple), it is then
        treated as:
        
            # il = (i1, i2, i3)
            foo(a, b, i1, i2, i3) => foo(a, b, i for i in (i1, i2, i3))
        Ex.
            Consider ints a and b, index-list il and operation @.
            il = [1,3,4,5], asuperior = False
            ---------------------------------
            a  b  @  mask  result
            1  1  x  0     0
            0  1  x  1     x
            1  1  x  0     0
            0  0  x  1     x
            0  1  x  1     x
            1  0  x  1     x

        If no indices are applied the operation is done one all bits.

        The method for keeping values unsigned is,
            - value: may be any number (1 << x) where x in range(self.nbit)
            - ADD self.senior -> Since it is always true senior > x, the
            summand must be positive.
            - AND self.g_mask -> Remove any bits outside what is allowed.
        """

        self.nbit = nbit
        self.senior = 1 << nbit
        self.g_mask = self.senior - 1
        self.asuperior = asup

    def notAt(self, a, *il):
        """Bitwise operation NOT on bits il."""
        if not il:
            return ~a + self.senior & self.g_mask
        for i in il:
            mask = 1 << i
            n_mask = mask ^ self.g_mask
            # Use truthy/falsey property of bools
            a = (a & n_mask) if a & mask else (a | mask)
        return a

    def andAt(self, a, b, *il):
        """Bitwise operation AND on bits il."""
        c = a if self.asuperior else 0
        if not il:
            return (a & b) + self.senior & self.g_mask
        return self.moveAt(c, a & b, *il)

    def nandAt(self, a, b, *il):
        """Bitwise operation NAND on bits il."""
        c = a if self.asuperior else 0
        if not il:
            return ~(a & b) + self.senior & self.g_mask
        return self.moveAt(c, ~(a & b), *il)

    def orAt(self, a, b, *il):
        """Bitwise operation OR on bits il."""
        c = a if self.asuperior else 0
        if not il:
            return (a | b) + self.senior & self.g_mask
        return self.moveAt(c, a | b, *il)

    def norAt(self, a, b, *il):
        """Bitwise operation NOR on bits il."""
        c = a if self.asuperior else 0
        if not il:
            return ~(a | b) + self.senior & self.g_mask
        return self.moveAt(c, ~(a | b), *il)

    def xorAt(self, a, b, *il):
        """Bitwise operation XOR on bits il."""
        c = a if self.asuperior else 0
        if not il:
            return (a ^ b) + self.senior & self.g_mask
        return self.moveAt(c, a ^ b, *il)

    def xnorAt(self, a, b, *il):
        """Bitwise operation XNOR on bits il."""
        c = a if self.asuperior else 0
        if not il:
            return ~(a ^ b) + self.senior & self.g_mask
        return self.moveAt(c, ~(a ^ b), *il)

    def highAt(self, a, *il):
        """Bitwise operation HIGH on bits il."""
        if not il:
            return self.g_mask
        for i in il:
            a |= 1 << i
        return a

    def lowAt(self, a, *il):
        """Bitwise operation LOW on bits il."""
        if not il:
            return 0
        for i in il:
            a &= (1 << i) ^ self.g_mask
        return a

    def moveAt(self, a, b, *il):
        """
        Will move bits il from b to a.

        if a[i] means bit i in a,
        Algorithm:
            for i in il, move b[i] to a[i]
            return a

        Is per definition always asuperior.
        """
        if not il:
            return a
        mask = 0
        for i in il:
            mask |= 1 << i
        n_mask = mask ^ self.g_mask
        return (a & n_mask) | (b & mask)

    def represent(self, a):
        """return a tuple of bools representative of value."""
        return tuple(bool(a & 1 << i) for i in range(self.nbit))

    def getWhereHigh(self, a):
        """Return a tuple of indices of all bits that are high."""
        return tuple(i for i in range(self.nbit) if a & 1 << i)

    def getWhereLow(self, a):
        """Return a tuple of indices of all bits that are low."""
        return tuple(i for i in range(self.nbit) if not a & 1 << i)
        
    def isHighAt(self, a, *il):
        """Returns true if all indices in il are high."""
        return all(a & 1 << i for i in il)

    def isLowAt(self, a, il):
        """Returns true if all indices in il are low."""
        return not any(a & 1 << i for i in il)

    def haseven(self, a):
        """Returns true if there is a even amount of 1s in a."""
        return sum(self.getWhereHigh(a)) % 2 == 0
