def unique(items):
    '''Remove duplicate items from a sequence, preserving order

    >>> unique([1, 2, 3, 2, 1, 4, 2])
    [1, 2, 3, 4]
    >>> unique([2, 2, 2, 1, 1, 1])
    [2, 1]
    >>> unique([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> unique([])
    []
    '''
    seen = set()

    def is_new(obj, seen=seen, add=seen.add):
        if obj in seen:
            return 0
        add(obj)
        return 1

    return filter(is_new, items)
