#!/usr/bin/env python

'''Make sure our atexit handler are called even on signals'''

__author__ = 'Miki Tebeka <miki.tebeka@gmail.com>'

from signal import signal, SIGTERM, SIGINT
import atexit


def signal_handler(signum, stackframe):
    '''Just make sure we exit gracefully'''
    raise SystemExit


def install_exit_handler(exit_func):
    for signum in (SIGTERM, SIGINT):
        signal(signum, signal_handler)
    atexit.register(exit_func)


if __name__ == '__main__':
    from os import kill, getpid

    def bye():
        print('BYE')

    install_exit_handler(bye)

    print('''
    Cause suicide is painless
    it brings on many changes
    and I can take or leave it if I please.

    ...and you can do the same thing if you please.
        - M.A.S.H.
    ''')

    kill(getpid(), SIGTERM)
