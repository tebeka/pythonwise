#!/usr/bin/env python
'''Parallel map (Unix only)'''
# The big advantage of this implemetation is that "fork" is very fast on
# copying data, so if you pass big arrays as arguments and return small values
# this is a win

from os import fork, pipe, fdopen, waitpid, P_WAIT
from marshal import dump, load
from itertools import takewhile, count

def spawn(func, data):
    read_fo, write_fo = map(fdopen, pipe(), ("rb", "wb"))
    pid = fork()
    if pid:
        return pid, read_fo

    dump(func(data), write_fo)
    write_fo.close()
    raise SystemExit

def wait(child):
    pid, fo = child
    waitpid(pid, P_WAIT)
    return load(fo)

# FIXME: For too many items, we get "Too many open files"
def pmap(func, items):
    '''
    >>> pmap(lambda x: x * 2, range(5))
    [0, 2, 4, 6, 8]
    '''
    children = map(lambda item: spawn(func, item), items)
    return map(wait, children)

if __name__ == "__main__":
    def fib(n):
        a, b = 1, 1
        while n > 1:
            a, b = b, a + b
            n -= 1
        return b

    items = range(10)
    print "pmap(fib, %s)" % str(items)
    print pmap(fib, items)

