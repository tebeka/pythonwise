#!/usr/bin/env python
'''Show download url for installed packages.'''

from pip.util import get_installed_distributions


def download_url(dist):
    '''Get download url from distribution PKG-INFO file.'''
    for line in dist._get_metadata('PKG-INFO'):
        if line.startswith('Download-URL:'):
            return line.split(':', 1)[1]


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(
        description='show download urls for installed packages')
    parser.add_argument('--unknown', help='show unknown urls',
                        action='store_true', default=False)
    args = parser.parse_args(argv[1:])

    for dist in get_installed_distributions():
        url = download_url(dist)
        if url or args.unknown:
            print('{}: {}'.format(dist.project_name, url or 'UNKNOWN'))


if __name__ == '__main__':
    main()
