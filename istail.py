from itertools import chain

def istail(it):
    '''Check if iterator has exactly one more element.
    Return True/False and iterator.'''
    try:
        i = next(it)
    except StopIteration:
        return False, it

    try:
        j = next(it)
        return False, chain([i, j], it)
    except StopIteration:
        return True, chain([i], it)

def ipeek(it):
    '''Peek into iterator, return first element and iterator.'''
    item = next(it)
    return item, chain([item], it)

def _test():
    t, it = istail(iter([]))
    print(t, list(it))
    t, it = istail(iter([1]))
    print(t, list(it))
    t, it = istail(iter([1, 2]))
    print(t, list(it))

    items = (i for i in range(5))
    i, items = ipeek(items)
    print(i, list(items))

if __name__ == '__main__':
    _test()
