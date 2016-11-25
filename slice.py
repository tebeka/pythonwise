# Example on using slice object for indexing


def fn1(items, use_tail=False):
    if use_tail:
        key = items[-2:]
    else:
        key = items[0]

    print(key)


items = [1, 2, 3, 4, 5]
fn1(items)
fn1(items, True)


def fn2(items, use_tail=False):
    idx = slice(-2, None) if use_tail else 0
    key = items[idx]

    print(key)


items = [1, 2, 3, 4, 5]
fn2(items)
fn2(items, True)
