#! /usr/bin/env python3

def add(l1, l2):
    return [a+b for a,b in zip(l1, l2)]
def sub(l1, l2):
    return [a-b for a,b in zip(l1, l2)]



class CartVec(object):

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, keys):
        if type(keys) is tuple:
            for key in keys:
                assert type(key) is int, ("Tuple indices in vector-like "
                                          "objects must be integers.")
            return tuple(self[key] for key in keys)
        elif type(keys) is slice:
            return ([self.x, self.y, self.z])[keys]
        elif type(keys) is int:
            if keys == 0:
                return self.x
            elif keys == 1:
                return self.y
            elif keys == 2:
                return self.z
            else:
                return NotImplemented   
        else:
            raise Exception("Vector-like indices must be tuples, slices "
                            "or integers.")
    
    def __iter__(self):
        return iter([self.x, self.y, self.z])
            
    def __add__(self, other):
        if (type(other) is self.__class__ or 
            issubclass(type(other), (list, tuple))):
            assert len(other) <= 3, ("Vector-like object cannot "
                                     "have more than 3 coordinates.")
            return self.__class__(x = self.x + other[0],
                                  y = self.y + other[1],
                                  z = self.z + other[2])
        else:
            return NotImplemented

    def __sub__(self, other):
        if (type(other) is self.__class__ or 
            issubclass(type(other), (list, tuple))):
            assert len(other) <= 3, ("Vector-like object can't "
                                     "have more than 3 coordinates.")
            return self.__class__(x = self.x - other[0],
                                  y = self.y - other[1],
                                  z = self.z - other[2])
        else:
            return NotImplemented

    __rmul__ = __mul__
    def __mul__(self, other):
        if type(other) is self.__class__:
            return sum(a*b for a, b in zip(self, other))
        elif issubclass(type(other), (list, tuple)):
            assert len(other) <= 3, ("Vector-like object can't "
                                     "have more than 3 coordinates.")
            return sum(a*b for a, b in zip(self, other))
        elif type(other) is int:
            return self.__class__(x = self.x * other,
                                  y = self.y * other,
                                  z = self.z * other)
        else:
            return NotImplemented

    def __pow__(self, other):
        if type(other) is int:
            if other % 2:
                # odd
                return (self*self)**(other//2) * self
            else:
                return (self*self)**(other//2)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        return self.__class__(self.x / other,
                              self.y / other,
                              self.z / other)
        
    


    """
    def __truediv__(self, other)
    def __floordiv__(self, other)
    def __mod__(self, other)
    def __divmod__(self, other)
    def __pow__(self, other[, modulo])
    def __lshift__(self, other)
    def __rshift__(self, other)
    def __and__(self, other)
    def __xor__(self, other)
    def __or__(self, other)
    """
