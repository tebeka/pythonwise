#!/usr/bin/env python
'''Parallel map (Unix only)'''

# The big advantage of this implementation is that "fork" is very fast on
# copying data, so if you pass big arrays as arguments and return small values
# this is a win

# FIXME
# * For too many items, we get "Too many open files"
# * Handle child exceptions

from functools import partial
from marshal import dump, load
from os import fork, pipe, fdopen, waitpid, P_WAIT


def spawn(func, data):
    read_fo, write_fo = map(fdopen, pipe(), ('rb', 'wb'))
    pid = fork()
    if pid:  # Parent
        return pid, read_fo

    # Child
    dump(func(data), write_fo)
    write_fo.close()
    raise SystemExit


def wait(child):
    pid, fo = child
    waitpid(pid, P_WAIT)
    value = load(fo)
    fo.close()
    return value


def pmap(func, items):
    """Parallel map (using fork) of func over items
    >>> pmap(lambda x: x * 2, range(5))
    [0, 2, 4, 6, 8]
    """
    children = map(partial(spawn, func), items)
    return map(wait, children)


if __name__ == '__main__':
    def fib(n):
        a, b = 1, 1
        while n > 1:
            a, b = b, a + b
            n -= 1
        return b

    nums = range(10)
    print('pmap(fib, %s)' % str(nums))
    for num, val in zip(nums, pmap(fib, nums)):
        print('%d -> %d' % (num, val))
