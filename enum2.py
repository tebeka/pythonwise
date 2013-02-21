'''Yet another enum implemenation.'''
from collections import namedtuple


def enum(*fields, **kw):
    '''Return an object where each field is mappend to its location.

    You can specify `bitmask` keyword, then fields are mapped to bitwise
    location (for bit masks).
    '''
    op = (lambda x: 1 << x) if kw.get('bitmask', False) else (lambda x: x)
    return namedtuple('Enum', fields)(*(op(i) for i, _ in enumerate(fields)))


def _test():
    Colors = enum('Red', 'Green', 'Blue')
    print(Colors.Green)  # 1

    Interrupts = enum('TERM', 'KILL', 'HUP', 'INT', bitmask=True)
    print(Interrupts.HUP)  # 4


if __name__ == '__main__':
    _test()
