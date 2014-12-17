#!/usr/bin/env python
'''Display some validation statistics on points_pre vs points_post data.'''

from pandas import HDFStore

def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='show some statistics')
    parser.parse_args(argv[1:])

    store = HDFStore('points.h5')
    pre, post = store['pre'], store['post']

    # Calculate diff in %
    diff = (pre - post)/pre * 100

    # Initial statistics
    print(diff.describe())


if __name__ == '__main__':
    main()

