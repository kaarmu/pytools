#! /usr/bin/env python3

from functools import reduce
import operator as op

from collections.abc import Container

def ispower2(x):
    if x == 0:
        return -1
    elif x == 1:
        return 0
    elif x % 2:
        return -1
    else:
        return ispower2(x // 2) + 1 or -1


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

class blis(Container):
    """A binary list. Represents a set of bits in list format with bools."""
    def __init__(self, *args):
        
        self.value = []
        
        if len(args) == 1:
            ls, = args
            
            if type(ls) in (list, tuple):
                for x in ls:
                    if type(x) is not bool:
                        raise TypeError(f"Elements must be bool, not {type(x)}.")
                    self.value.append(x)
            else:
                raise TypeError(f"Cannot create blis out of {type(ls)}.")

        elif len(args) == 2:
            nbit, x = args

            if type(x) is int:
                self.value = list(BinT(nbit).partition(x))
            else:
                raise TypeError(f"Cannot create blis out of {type(x)}.")

        else:
            raise TypeError('Expected either one argument with list or tuple of bools, '
                            'or two arguments ')

    def push(self, x):
        if type(x) is not bool:
            raise TypeError(f"Elements must be bool, not {type(x)}.")

        return self.value.append(x)
      
    def pop(self):
        return self.value.pop()

    def insert(self, i, x):
        if type(x) is not bool:
            raise TypeError(f"Elements must be bool, not {type(x)}.")

        return self.value.insert(i, x)
    
    def extend(self, x):
        if type(ls) in (list, tuple):
            for x in ls:
                if type(x) is not bool:
                    raise TypeError(f"Elements must be bool, not {type(x)}.")
                self.value.append(x)
        else:
            raise TypeError(f"Cannot extend blis out of {type(ls)}.")

    def reverse(self):
        return 

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)

    def __str__(self):
        return ''.join(f'{bit}' if i%4 else f' {bit}' for i, bit in enumerate(self.value))
    
    # __hash__: None  # type: ignore
    
    def __getitem__(self, i):
        if type(i) not in (int, slice):
            raise Exception(f'Index must be either int or slice, not {type(i)}.')
        
        return self.value[i]

    def __setitem__(self, i, x):
        if type(i) not in (int, slice):
            raise Exception(f'Index must be either int or slice, not {type(i)}.')
        
        if type(x) is not bool:
            raise Exception(f'Elements must be bool, not {type(x)}.')
        
        return self.value[i] = x

    def __delitem__(self, i):
        if type(i) not in (int, slice):
            raise Exception(f'Index must be either int or slice, not {type(i)}.')

        del self.value[i]

    def __add__(self, x):
        # Concat 
        if type(x) is bool:
            self.push(x)
        elif type(x) in (list, tuple):
            self.extend(x)
        else:
            return NotImplemented



    # SAME AS OR
    # def __add__(self, x: List[_T]) -> List[_T]: ...
    # USELESS; x+x=x
    # def __iadd__(self: _S, x: Iterable[_T]) -> _S: ...
    # SAME AS AND
    # def __mul__(self, n: int) -> List[_T]: ...
    # def __rmul__(self, n: int) -> List[_T]: ...
    # CONTAIN A SEQUENCE
    # def __contains__(self, o: object) -> bool: ...
    # REVERSE
    # def __reversed__(self) -> Iterator[_T]: ...
    # def __gt__(self, x: List[_T]) -> bool: ...
    # def __ge__(self, x: List[_T]) -> bool: ...
    # def __lt__(self, x: List[_T]) -> bool: ...
    # def __le__(self, x: List[_T]) -> bool: ...

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

    def partition(self, a):
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

    def iseven(self, a):
        """Returns true if there is a even amount of 1s in a."""
        return sum(self.getWhereHigh(a)) % 2 == 0
