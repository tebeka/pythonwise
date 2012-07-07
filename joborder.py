#!/usr/bin/env python
'''Show dependencies of Azkaban jobs.

You'll need graphviz "dot" utility in your path.
'''

from glob import glob
import re
from os.path import isdir, join, basename
from tempfile import NamedTemporaryFile
from subprocess import call
from sys import platform


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='Show job order in directory')
    parser.add_argument('directory', help='jobs directory [.]', default='.',
                       nargs='?')
    parser.add_argument('--keep', help='keep intermediate dot file',
                        action='store_true', default=False)
    args = parser.parse_args(argv[1:])

    if not isdir(args.directory):
        raise SystemExit('error: {} is not a directory'.format(args.directory))

    jobfiles = glob(join(args.directory, '*.job'))
    if not jobfiles:
        raise SystemExit('error: no *.job files in {}'.format(args.directory))

    find_dep = re.compile('dependencies=(\w+)').search


    dotfile = NamedTemporaryFile(delete=not args.keep, suffix='.dot')
    if args.keep:
        print('dot file at {}'.format(dotfile.name))

    dotfile.write('digraph G {\n')
    for jobfile in jobfiles:
        name = basename(jobfile)[:-4]
        with open(jobfile) as fo:
            match = find_dep(fo.read())

        if not match:
            continue
        dotfile.write('    {} -> {};\n'.format(name, match.group(1)))
    dotfile.write('}\n')
    dotfile.flush()

    image = '/tmp/job-deps.png'

    if call(['dot', '-Tpng', '-o', image, dotfile.name]) != 0:
        raise SystemExit(
            'error: cannot run dot on {} (PATH problem?)'.format(dotfile.name))

    cmd = {
        'darwin': 'open',
        'linux2': 'xdg-open',
        'win32': 'start',
    }[platform]

    if call([cmd, image]) != 0:
        raise SystemExit('error: cannot show {}'.format(image))

if __name__ == '__main__':
    main()

