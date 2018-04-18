from time import monotonic, sleep
from functools import wraps


def timed(fn):
    """Timing decorator"""
    @wraps(fn)
    def wrapper(*args, **kw):
        start = monotonic()
        try:
            return fn(*args, **kw)
        finally:
            duration = monotonic() - start
            print('{} took {:.2f}sec'.format(fn.__name__, duration))
    return wrapper


@timed
def add(a, b):
    """Does addition"""
    sleep(a/10.0)  # Simulate work
    return a + b
