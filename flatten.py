#!/usr/bin/env python

__author__ = "Miki Tebeka <miki.tebeka@gmail.com>"

def flatten(items):
    '''Flatten a nested list.

    >>> a = [[1], 2, [[[3]], 4]]
    >>> list(flatten(a))
    [1, 2, 3, 4]
    >>> 
    '''
    for item in items:
        if getattr(item, "__iter__", None):
            for subitem in flatten(item):
                yield subitem
        else:
            yield item

if __name__ == "__main__":
    from doctest import testmod
    testmod()
