# A simple timer to time portions of your code

from sys import stdout
from time import time

class Timer(object):
    def __init__(self, name, log=None):
        '''name: timer name
           log: log function, most probably logger.info
        '''
        self.name = name
        self.log = log or (lambda message: stdout.write(message + '\n'))

    def __enter__(self):
        self.start = time()
        self.log('[{}] started'.format(self.name))

    def __exit__(self, type, value, traceback):
       duration = time() - self.start
       self.log('[{}] ended in {:.3f} seconds'.format(self.name, duration))


if __name__ == '__main__':
    from time import sleep

    # This will print something like
    #   [test] started
    #   [test] ended in 1.702 seconds
    with Timer('test'):
        sleep(1.7)

