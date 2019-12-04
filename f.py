"""f-strings in Python 2"""
from inspect import currentframe, getouterframes


# Sadly, Python 2 doesn't have ChainMap
def chain_maps(*maps):
    cm = {}
    for m in reversed(maps):
        cm.update(m)
    return cm


def f(s):
    """Format s with parameter from environment

    >>> x = 123
    >>> f('x = {x}')
    'x = 123'
    """
    caller = getouterframes(currentframe(), 2)[1][0]
    return s.format(**chain_maps(caller.f_locals, caller.f_globals))
