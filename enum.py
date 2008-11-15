#!/usr/bin/env python

def enum(*names, **kw):
    '''
    >>> flags = enum("A", "B", "C")
    >>> flags.A
    1
    >>> flags.C
    3
    >>> flags = enum("A", "B", "C", bitmask=1)
    >>> flags.A
    1
    >>> flags.C
    4
    '''
    class Enum: pass
    value = (lambda i: 1 << i) if kw.get("bitmask", 0) else (lambda i: i + 1)

    enum = Enum()
    for i, name in enumerate(names):
        setattr(enum, name, value(i))

    return enum

if __name__ == "__main__":
    from doctest import testmod
    testmod(verbose=1)
