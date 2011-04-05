#!/usr/bin/env python
'''Simplify creating decorators with optional parameters'''

from functools import wraps
from time import ctime

def logged(fn, name=None):
    '''Decorator to "log" function start and end. It can be used either in
    "bare" format
    @logged
    def f():
        pass

    or with a "name" parameter
    @logged("foo")
    def f():
        pass
    '''

    # @logged("foo") used
    if isinstance(fn, basestring):
        return lambda f: logged(f, fn)

    # @logged used
    name = name or "{0}.{1}".format(__name__, fn.__name__)

    @wraps(fn)
    def wrapped(*args, **kw):
        print("[{0}] - {1} - START".format(ctime(), name))
        value = fn(*args, **kw)
        print("[{0}] - {1} - END".format(ctime(), name))

        return value
    return wrapped

if __name__ == "__main__":
    @logged("blah")
    def f(x):
        print("f: {0}".format(x))

    @logged
    def g(x):
        print("g: {0}".format(x))


    f(8)
    g(7)
