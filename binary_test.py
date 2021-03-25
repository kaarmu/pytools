#! /usr/bin/env python3

from unittest import TestCase, TestSuite,  main

from binary import blis
import operator


operands = [
    (+5, +500),
    (+500, +5),
    (+5, -500),
    (-5, +500),
    (+500, -5),
    (-500, +5),
    (-5, -500),
    (-500, -5),
    ]
cast = [
    # (int, int),
    (int, blis),
    (blis, int),
    (blis, blis)
]

def operator_test(self):
    for lopand, ropand in operands:

        ans = self.op(lopand, ropand)

        for cl, cr in cast:

            errmsg = f'{cl.__name__}({lopand})'
            errmsg += f' {self.op.__name__} '
            errmsg += f'{cr.__name__}({ropand})'

            left = cl(lopand)
            right = cr(ropand)

            est = self.op(left, right)

            with self.subTest():
                self.assertEqual(int(est), ans, errmsg)
            
            print(errmsg, 'complete!', f'ans: {ans}', f'est: {int(est)}')


class BLIS_ADD(TestCase):
    def test(self):
        self.op = operator.add
        operator_test(self)
        

class BLIS_SUB(TestCase):
    def test(self):
        self.op = operator.sub
        operator_test(self)

class BLIS_MUL(TestCase):
    def test(self):
        self.op = operator.mul
        operator_test(self)


class BLIS_DIV(TestCase):
    def test(self):
        self.op = operator.floordiv
        operator_test(self)

class BLIS_MOD(TestCase):
    def test(self):
        self.op = operator.mod
        operator_test(self)

class BLIS_POW(TestCase):
    def test(self):
        self.op = operator.pow
        operator_test(self)


if __name__ == '__main__':
    main()