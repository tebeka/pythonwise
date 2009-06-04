#!/usr/bin/env python
'''Quick and dirty object "repr"'''

__author__ = "Miki Tebeka <miki.tebeka@gmail.com>"

# FIXME: Find how to make doctest play with "regular" class definition

def printobj(obj):
    '''
    Quick and dirty object "repr"

    >>> class Point: pass
    >>> p = Point()
    >>> p.x, p.y = 1, 2
    >>> printobj(p)
    ('y', 2)
    ('x', 1)
    >>>
    '''
    print "\n".join(map(str, obj.__dict__.items()))

if __name__ == "__main__":
    from doctest import testmod
    testmod()
