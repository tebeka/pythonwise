'''Sending metrics to statsd server.

We define `metered` context manager and `metrics` decorator. Both will update
the following metrics:

    # Counters
    - <prefix>.<name>.num_runs
    - <prefix>.<name>.num_failed
    - <prefix>.<name>.num_passed

    # Timers
    - <prefix>.<name>

StatsD server, port and <prefix> are defined in the config module.

Example::

    import sdmetrics
    sdmetrics.setup(prefix='math')

    @metrics
    def add(x, y):
        return x + 7


Will result in the following metrics:
    * stats.counters.math.add.num_runs
    * stats.counters.math.add.num_failed
    * stats.counters.math.add.num_passed
    * stats.timers.math.add.*

This package depends on "statsd" package.
'''

from statsd import StatsClient

from functools import wraps
from time import time

_prefix = 'sdmetrics'
_statsd_host = 'localhost'
_statsd_port = 8125


def setup(prefix=None, statsd_host=None, statsd_port=None):
    global _prefix, _statsd_host, _statsd_port

    _prefix = prefix or _prefix
    _statsd_host = statsd_host or _statsd_host
    _statsd_port = statsd_port or _statsd_port


def get_client():
    return StatsClient(_statsd_host, _statsd_port)


class metered(object):
    '''A context manager sending metrics to statsd.

    Usage:

        with metered('summary'):
            cursor.execute(summary_sql)
    '''
    def __init__(self, name):
        prefix = '{}.{}'.format(_prefix, name)
        self.runs = '{}.num_runs'.format(prefix)
        self.fail = '{}.num_failed'.format(prefix)
        self.passed = '{}.num_passed'.format(prefix)
        self.time = prefix
        self.client = get_client()

    def __enter__(self):
        self.client.incr(self.runs)
        self.start = time()

    def __exit__(self, exc_type, exc_value, traceback):
        client = self.client

        duration = int(time() - self.start) * 1000  # statsd times in msec
        client.timing(self.time, duration)
        key = self.passed if exc_type is None else self.fail
        client.incr(key)


def metrics(fn):
    '''A decorator manager sending metrics to statsd.

    Usage:

        @metrics
        def add(x, y):
            return x + y

    '''
    name = fn.__name__

    @wraps(fn)
    def wrapper(*args, **kw):
        with metered(name):
            return fn(*args, **kw)

    return wrapper
