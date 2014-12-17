'''Metrics library.

Metrics are thread safe values.
You can expose metrics with serve_http method.
'''

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from cStringIO import StringIO
from operator import add, sub
from threading import RLock, Thread
import json
from time import sleep, time

_LOCK = RLock()
_METRICS = {}

class Metric:
    '''Metric class

    This class exposes `get` and `set` which are both thread safe.
    '''
    def __init__(self, name, value=None):
        with _LOCK:
            if name in _METRICS:
                raise ValueError('metric {0} alreay exists'.format(name))
            _METRICS[name] = self
        self.name = name
        self.value = value
        self.lock = RLock()

    def set(self, value):
        with self.lock:
            self.value = value

    def get(self):
        return self.value

class NumericMetric(Metric):
    '''NumericMetric has inc and dec methods, good for counters.'''
    def __init__(self, name, value=0, step=1):
        Metric.__init__(self, name, value)
        self.step = step

    def _op(self, func, step):
        step = step if step is not None else self.step
        with self.lock:
            self.set(func(self.get(), step))

    def inc(self, step=None):
        self._op(add, step)

    def dec(self, step=None):
        self._op(sub, step)


class TimerMetric(Metric):
    '''Timer metric. Show elapsed time from start until now or when `stop` was
    called.'''
    def __init__(self, name, start=None):
        Metric.__init__(self, name, start or time())
        self.end = None

    def stop(self, end=None):
        with self.lock:
            self.end = end or time()

    def get(self):
        end = self.end or time()
        return end - self.value


# Get a metric
def get(name):
    with _LOCK:
        return _METRICS.get(name)

def getval(name):
    '''Get value of metric.'''
    return get(name).get()

def iter_metrics():
    '''Iterate over metrics, return list of `(name, value)` tuples'''
    with _LOCK:
        return [(name, getval(name)) for name in _METRICS]

def as_json(out=None):
    '''Metrics as JSON object.

    If out is None will return string, otherwise will dump to fo.
    '''
    fo = out if out else StringIO()
    json.dump(dict(iter_metrics()), fo)

    if not out:
        return fo.getvalue()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        as_json(self.wfile)
        self.wfile.write('\n')
        self.wfile.close()

    # Be quiet
    def log_message(self, format, *args):
        pass

def serve_metrics(port):
    '''Serve metrics via HTTP/JSON on port.'''

    server = HTTPServer(('localhost', port), Handler)
    server.allow_reuse_address = True

    t = Thread(target=server.serve_forever)
    t.daemon = True
    t.start()

    return server


def _test():
    from random import randint
    default_port = 9999

    from argparse import ArgumentParser
    parser = ArgumentParser('Metrics HTTP server')
    parser.add_argument('-p', '--port', default=default_port, type=int,
                        help='port to listen on ({0})'.format(default_port))

    args = parser.parse_args()
    serve_metrics(args.port)

    metric = Metric('metric')
    numeric = NumericMetric('numeric')
    TimerMetric('timer')

    def mutate_thread():
        while True:
            numeric.inc()
            metric.set(randint(0, 100))
            sleep(0.1)

    t = Thread(target=mutate_thread)
    t.daemon = True
    t.start()

    print('Serving metrics at http://localhost:{}'.format(args.port))
    # There's no way to "join" a server
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    _test()
