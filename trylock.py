from functools import wraps
from threading import RLock
from collections import defaultdict

class AlreadyRunningError(Exception):
    pass


def try_lock(keyfn=None):
    '''Allow function to run only once. `keyfn` can be used to select a subset
    of the function arguments/kwargs to lock on.

    Will raise `AlreadyRunningError` if runtion already running.

    Example::
        def push(day, records):
            ...

    And we care only about the day argument, when we'll do::

        @try_lock(lambda args, kw: args[0])
        def push(day, records):
            ...
    '''
    by_key_locks = defaultdict(RLock)
    master_lock = RLock()

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kw):
            key = keyfn(args, kw)

            # Get lock for key
            with master_lock:
                lock = by_key_locks[key]

            if not lock.acquire(blocking=False):
                raise AlreadyRunningError(
                    "{} already running for {}".format(func.__name__, key))

            try:
                return func(*args, **kw)
            finally:
                lock.release()
        return wrapped
    return wrapper
