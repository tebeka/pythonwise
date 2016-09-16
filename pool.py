"""Simple Pool object"""

from queue import Queue


class Proxy:
    """Wraps original object with context manager that return the object to the
    pool."""
    def __init__(self, obj, pool):
        self._obj = obj
        self._pool = pool

    def __enter__(self):
        return self._obj

    def __exit__(self, typ, val, tb):
        self._pool._put(self._obj)


class Pool:
    """Pool of objects"""
    def __init__(self, objects):
        self._queue = Queue()
        for obj in objects:
            self._queue.put(obj)

    def get(self):
        """Get object from the pool, should be used as contect manger. e.g.:

            with pool.get() as conn:
                cur = conn.cursor()
                cur.execute('SELECT ...')
        """
        return Proxy(self._queue.get(), self)

    def _put(self, obj):
        self._queue.put(obj)


if __name__ == '__main__':
    from threading import Thread, Barrier
    from time import sleep
    from random import random

    n = 10
    b = Barrier(n)
    p = Pool([1, 2, 3])

    def worker(n, barrier, pool):
        barrier.wait()  # Wait for all threads to be ready
        sleep(random() / 10)
        with pool.get() as val:
            print('worker %d got resource %d' % (n, val))

    for i in range(n):
        Thread(target=worker, args=(i, b, p)).start()
