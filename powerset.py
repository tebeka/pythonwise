def power_set(iterable):
    """Yields the power set of iterable (including the empty set)"""
    items = list(iterable)
    nitems = len(items)
    for n in range(2**nitems):
        # Use n as bitmask to pick items
        yield [items[bit] for bit in range(nitems) if (n >> bit) & 1]
