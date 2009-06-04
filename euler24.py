#!/usr/bin/env python
''' Solving http://projecteuler.net/index.php?section=problems&id=24

Note that Python's 2.6 itertools.permutations return the permutation in order so
we can just write:
    from itertools import islice, permutations
    print islice(permutations(range(10)), 999999, None).next()

And it'll work much faster :)
'''

from itertools import islice, ifilter

def is_last_permutation(n):
    return n == sorted(n, reverse=1)

def next_head(n):
    '''Find next number to be 'head'. 

    It is smallest number if the tail that is bigger than the head.
    In the case of (2 4 3 1) it will pick 3 to get the next permutation
    of (3 1 2 4)
    '''
    return sorted(filter(lambda i: i > n[0], n[1:]))[0]

def remove(element, items):
    return filter(lambda i: i != element, items)

def next_permutation(n):
    if is_last_permutation(n):
        return None

    sub = next_permutation(n[1:])
    if sub:
        return [n[0]] + sub

    head = next_head(n)
    return [head] + sorted([n[0]] + remove(head, n[1:]))

def nth(it, n):
    '''Return the n'th element of an iterator'''
    return islice(it, n, None).next()

def iterate(func, n):
    '''iterate(func, n) -> n, func(n), func(func(n)) ...'''
    while 1:
        yield n
        n = func(n)

def permutations(n):
    return ifilter(None, iterate(next_permutation, n))

if __name__ == "__main__":
    n = range(10)
    m = 1000000
    print "Calculateing the %d permutation of %s" % (m, n)
    print nth(permutations(n), m-1)
