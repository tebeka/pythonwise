import zmq
import pickle
from itertools import repeat

port = 50000

_ctx = zmq.Context()
_sock = _ctx.socket(zmq.PUB)
_sock.bind('tcp://127.0.0.1:{}'.format(port))


def encode(type, message):
    return '{} {}'.format(type, pickle.dumps(message))


def decode(message):
    type, payload = message.split(' ', 1)
    return type, pickle.loads(payload)


def publish(type, message):
    _sock.send(encode(type, message))


def subscribe(type, callback=None, host=None):
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    host = host or '127.0.0.1'
    sock.connect('tcp://{}:{}'.format(host, port))
    sock.setsockopt(zmq.SUBSCRIBE, type)

    queue = (decode(sock.recv()) for _ in repeat(None))

    if callback:
        for type, message in queue:
            callback(type, message)
    else:
        return queue


def _test():
    from time import sleep
    from random import choice, random
    from threading import Lock, Thread

    def publisher():
        countries = ['netherlands','brazil','germany','portugal']
        events = ['yellow card', 'red card', 'goal', 'corner', 'foul']

        while True:
            type, message = choice(countries), choice(events)
            publish(type, message)
            sleep(random())

    thr = Thread(target=publisher)
    thr.daemon = True
    thr.start()

    plock = Lock()
    def log(message):
        with plock:
            print(message)

    class Reader(Thread):
        def __init__(self, type):
            Thread.__init__(self)
            self.type = type
            self.daemon = True

        def run(self):
            prefix = self.type or 'all'
            callback = lambda t, m: log('[{}] {}:{}'.format(prefix, t, m))
            subscribe(self.type, callback)

    # Subscribe to brazil
    thr = Reader('brazil')
    thr.start()

    # Subscribe to all events
    thr = Reader('')
    thr.start()


    sleep(20)

if __name__ == '__main__':
    _test()
