'''Example of class decorator to make sure some attributes are always Decimal'''

from decimal import Decimal
from operator import attrgetter

def decimals(cls):
    '''A class decorator that ensures all attributes specifiec in the class
    __decimals__ will be Decimal.

    Make sure your class is a new style class (inherits from object), otherwise
    this won't work.

    Example:
    >>> @decimals
    ... class Sale(object):
    ...     __decimals__ = ['price']
    ...     def __init__(self, item, price):
    ...         self.item = item
    ...         self.price = price
    ...
    >>> s1 = Sale('socks', 11.2)
    >>> type(s1.price)
    <class 'decimal.Decimal'>
    >>> s1.price = 70
    >>> type(s1.price)
    <class 'decimal.Decimal'>
    >>>
    '''
    def make_setter(name):
        def setter(self, value):
            setattr(self, name, Decimal(value))

        return setter

    for attr in cls.__decimals__:
        name = '_{}'.format(attr)
        getter = attrgetter(name)
        setter = make_setter(name)
        setattr(cls, attr, property(getter, setter, None, attr))

    return cls

if __name__ == '__main__':
    import doctest
    doctest.testmod()
