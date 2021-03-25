#! /usr/bin/env python3

"""
TODO:
    CRC
        Read,
        https://en.wikipedia.org/wiki/Cyclic_redundancy_check
        for similar project,
        https://en.wikipedia.org/wiki/Fletcher%27s_checksum
    Hamming code
    Revisit BinT
    Overflow problems of blis?
    blis from/to bytes
    blis setitem is suboptimal
"""

from numbers import Integral
from collections.abc import MutableSequence
from observation import isiterable


def ispower2(x):
    if x == 0:
        return -1
    elif x == 1:
        return 0
    elif x % 2:
        return -1
    else:
        return ispower2(x // 2) + 1 or -1

def ceilpow2(x, i=0):
    if 2**i < x:
        return ceilpow2(x, i+1)
    return i

def floorpow2(x, i=0):
    if 2**i <= x:
        if r := floorpow2(x, i+1):
            return r
        return i
    return None

def makeargblis(func):
    def wrapper(self, other):
        if type(other) is not type(self):
            other = blis(other)
        return func(self, other)
    return wrapper


class blis(Integral, MutableSequence):
    def __init__(self, *args):
        """
        Create a binary list of either an integer or iterable bools.

        blis(13, 4)
        [True, False, True, True] # index 0 -> LSB
        [1101]
        0b1101
        13

        Arguments:
            - blis(value)
            - blis(value, nbits)
            - blis(iterable)
            - blis(iterable, nbits)
            Types:
                value - int
                iterable - [tuple, list, ...]
                nbits - int
        """

        self.bits = []

        def from_value(val, nbits=None):
            neg = val < 0
            val = abs(val)
            
            if val == 0:
                nbits = nbits or 8
                self.bits = [0]*nbits
                return

            il = []
            while val:
                il.append(floorpow2(val))
                val -= 2**il[-1]
            m = max(il) + 2 # plus 2 because of zero indexing and one more for two's compl.
            nbits = nbits or max(m, 8)
            assert nbits > 0, 'nbits must be positive.'
            self.bits = [0]*nbits
            for i in il:
                if i < nbits:
                    self.bits[i] = 1
            if neg:
                self.negate()
 
        def from_sequence(seq, nbits=None):
            nbits = nbits or len(seq)
            assert nbits > 0, 'nbits must be positive.'
            for elm in seq:
                if type(elm) not in (bool, int):
                    raise TypeError(f'Expected elements of type bool, not {type(elm)}')
                if int(elm) not in (1, 0):
                    raise TypeError(f'Expected element to be one either [True, False, 1, 0], '
                                    f'not {elm}')
                self.bits.append(int(elm))

            self.bits = self.bits[:nbits] # if smaller nbits
            while len(self.bits) < nbits: # if larger nbits
                self.bits.append(0)

        def from_string(string, nbits=None):
            s = reversed(string)
            m = map(lambda x: int(x), s)
            l = list(m)
            for i in l:
                assert i in [0,1], 'int must be either 0 or 1.'
            from_sequence(l, nbits=nbits)

        if not args:
            return
        
        elif len(args) > 2:
            raise TypeError(f'Expected at most 2 arguments, not {len(args)}.')

        elif type(args[0]) is int:
            from_value(*args)

        elif type(args[0]) is str:
            from_string(*args)

        elif isiterable(args[0]):
            from_sequence(*args)
        
        else:
            raise TypeError(f'Expected first argument to be either '
                            f'int, list, tuple or blis, not {type(args[0])}.')

    #
    # PROPERTY
    #

    @property
    def nbits(self):
        return len(self.bits)

    @nbits.setter
    def nbits(self, n):
        if n > self.nbits:
            while len(self.bits) < n:
                self.bits.append(0)
        else:
            self.bits = self.bits[:n]

    @property
    def isneg(self):
        return bool(self.bits[-1]) if self.bits else True
    
    #
    # MODIFIERS
    #

    def negate(self):
        # invert self
        self.invert()
        # add one
        self.increment()
        return self

    def invert(self):
        for i, b in enumerate(self):
            self.bits[i] = int(not b)
        return self

    def increment(self):
        i, carry = 0, 1
        while carry and i < self.nbits:
            self.bits[i] = (self.bits[i] + carry) % 2
            if self.bits[i]:
                carry = 0
            i += 1
        if carry:
            self.bits.append(True)
        return self

    #
    # CONVERSION
    #

    def __repr__(self):
        return f"blis('{self!s}', {int(self)})"

    def __int__(self):
        value = sum(2**i for i, b in enumerate(self) if b)
        if self.isneg:
            value -= 2**self.nbits
        return value

    def __iter__(self):
        return iter(self.bits)

    def __str__(self):
        return ''.join(str(val) for val in reversed(self.bits))

    #
    # MATH OPERATORS
    #

    ## Unary

    def __pos__(self):
        # nothing more than copy self
        return blis(self)
    
    def __neg__(self):
        # copy and negate
        return blis(self).negate()

    ## Binary

    @makeargblis
    def __add__(self, other):
        nbits = max(self.nbits, other.nbits)
        val = int(self) + int(other) # easier to add in integers
        if 2**(nbits - 1) < val:
            nbits = None
        return blis(val, nbits)
    
    def __radd__(self, other):
        return self + other

    @makeargblis
    def __mul__(self, other):
        val = int(self) * int(other) # easier in integers
        return blis(val)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self / other

    def __rtruediv__(self, other):
        return other / self

    @makeargblis
    def __floordiv__(self, other):
        val = int(self) // int(other) # easier in integers
        return blis(val)
    
    @makeargblis
    def __rfloordiv__(self, other):
        val = int(other) // int(self)
        return blis(val)

    ## Special

    @makeargblis
    def __pow__(self, other):
        val = int(self) ** int(other) # easier in integers
        return blis(val)

    def __rpow__(self, arg):
        return NotImplemented

    @makeargblis
    def __mod__(self, other):
        val = int(self) % int(other) # easier in integers
        return blis(val, other.nbits)

    @makeargblis
    def __rmod__(self, other):
        val = int(other) % int(self)
        return blis(val, self.nbits)

    ## Functions

    def __abs__(self):
        return (-self) if self.isneg else (+self)

    def __ceil__(self):
        """
        Round up to any 2**n

        overflow error exist.
        if number is of 2**n, then returns 2**(n+1).
        for negative number, go to -2**(n-1).
        that is, move towards positive infinity.
        """
        if self.isneg:
            i = self.nbits - 1
            while self.bits[i] == 1:
                i -= 1
            other = blis(0, self.nbits)
            other.bits[i:] = [1] * (self.nbits - i)
        else:
            i = self.nbits - 1
            while self.bits[i] == 0:
                i -= 1
            other = blis(0, self.nbits)
            other.bits[i+1] = 1
        
        return other

    def __floor__(self):
        """
        Round down to any 2**n
        
        overflow error exist.
        same as ceil, but move towards negative infinity.
        """
        if self.isneg:
            i = self.nbits - 1
            while self.bits[i] == 1:
                i -= 1
            i += 1
            other = blis(0, self.nbits)
            other.bits[i:] = [1] * (self.nbits - i)
        else:
            i = self.nbits - 1
            while self.bits[i] == 0:
                i -= 1
            other = blis(0, self.nbits)
            other.bits[i] = 1
        
        return other

    def __trunc__(self):
        return self.__ceil__() if self.isneg else self.__floor__()

    def __round__(self, n):
        """
        Round to 2**n.

        I.e., remove/set-to-zero the first bits (from LSB).

        >> x = [11111111]
        >> round(x, 3)
        [11111000]
        """
        val = blis(self)
        for i in range(n):
            val.bits[i] = 0
        return val

    #
    # BIT OPERATORS
    #

    ## Unary

    def __invert__(self):
        # copy and invert
        return blis(self).invert()

    ## Binary

    @makeargblis
    def __and__(self, other):
        nbits = max(self.nbits, other.nbits)
        val = blis(self, nbits) # copy
        for i, bit in enumerate(other):
            val.bits[i] &= bit
        return val
    
    def __rand__(self, other):
        return self & other
    
    @makeargblis
    def __or__(self, other):
        nbits = max(self.nbits, other.nbits)
        val = blis(self, nbits) # copy
        for i, bit in enumerate(other):
            val.bits[i] |= bit
        return val

    def __ror__(self, other):
        return self | other

    @makeargblis
    def __xor__(self, other):
        nbits = max(self.nbits, other.nbits)
        val = blis(self, nbits)
        for i, bit in enumerate(other):
            val.bits[i] ^= bit
        return val
    
    def __rxor__(self, other):
        return self ^ other

    ## Special

    """
    PLAN:
    not me  int     <<      int     move arg1 left by arg2
    lshift  blis    <<      int     move arg1 left by arg2
    rlshift int     <<      blis    retreive the first arg1 bits of arg2
    lshift  blis    <<      blis    insert arg2 to the right of arg1

    not me  int     >>      int     move arg1 to the right by arg2
    rshift  blis    >>      int     retreive the first arg2 bits of arg1 from the right
    rrshift int     >>      blis    move arg2 to the right
    rshift  blis    >>      blis    insert 
    """

    def __lshift__(self, other):
        if type(other) is int:
            retval = blis()
            retval.bits = [0] * other + self.bits
            retval.nbits = self.nbits
        else:
            # self << other
            other = blis(other)
            
            retval = blis()
            retval.bits = other.bits + self.bits
            retval.bits = retval.bits[:self.nbits]

        return retval

    def __rlshift__(self, other):
        if type(other) is int:
            if other > self.nbits:
                raise TypeError('Argument cannot be larger than nbits.')
            retval = blis(self.bits[-other:])
        else:
            # other << self
            other = blis(other)
            
            retval = blis()
            retval.bits = self.bits + other.bits
            retval.bits = retval.bits[:other.nbits]

        return retval

    def __rshift__(self, other):
        if type(other) is int:
            if other > self.nbits:
                raise TypeError('Argument cannot be larger than nbits.')
            retval = blis(self.bits[:other])
        else:
            # self >> other
            other = blis(other)

            retval = blis()
            retval.bits = other.bits + self.bits
            retval.bits = retval.bits[-other.nbits:]
        
        return retval

    def __rrshift__(self, other):
        if type(other) is int:
            retval = blis()
            retval.bits = self.bits + [0] * other
            retval.bits = retval.bits[-self.nbits:]
        else:
            # other >> self
            other = blis(other)

            retval = blis()
            retval.bits = self.bits + other.bits
            retval.bits = retval.bits[-self.nbits:]

        return retval        

    #
    # COMPARISON
    #

    @makeargblis
    def __eq__(self, other):
        return int(self) == int(other)

    @makeargblis
    def __le__(self, other):
        return int(self) <= int(other)

    @makeargblis
    def __lt__(self, other):
        return int(self) < int(other)

    #
    # MANAGEMENT
    #

    def __len__(self, *args, **kwargs):
        return self.bits.__len__(*args, **kwargs)

    def __getitem__(self, i):
        return blis(self.bits[i])

    def __setitem__(self, *args, **kwargs):
        self.bits.__setitem__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        self.bits.__delitem__(*args, **kwargs)

    def insert(self, *args, **kwargs):
        self.bits.insert(*args, **kwargs)


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


class CRC:
    
    def __init__(self, poly):
        self.poly = blis(poly)
        self.order = self.poly.nbits
        self.poly.append(1)

    def write(self, x):

        x = blis(x)

        if x.nbits < self.poly.nbits:
            raise TypeError('x cannot have less number of bits than poly.')

        # padding with order
        x.bits = [0] * self.order + x.bits

        i = 0
        while x[self.order + 1:]:
            if x[-(i+1)] == 0:
                i += 1
                continue
            
            print(x)
            print(' '*i + str(self.poly))
            
            sl = slice(-(self.poly.nbits + i), -i or None)
            x[sl] = x[sl] ^ self.poly

        print(x)
        return x[:self.order]


