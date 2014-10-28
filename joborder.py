#!/usr/bin/env python
'''Show dependencies of Azkaban jobs.

Depenencies are in *.job files with a line starting with 'dependencies='.

You'll need graphviz "dot" utility in your path.
'''

from glob import glob
import re
from os.path import isdir, join, basename
from tempfile import NamedTemporaryFile
from subprocess import call
from sys import platform


def iter_dependencies(job_files, keep=False):
    '''Return a generator of (job, dep) from job_files.'''
    # Dependency line: dependencies=cooljob
    find_dep = re.compile('dependencies=(\w+)').search
    for job_file in job_files:
        name = basename(job_file)[:-4]
        with open(job_file) as fo:
            match = find_dep(fo.read())

            if not match:
                continue

            yield name, match.group(1)


def gen_image(dependencies, image):
    '''Generate an image from dependencies using "dot".'''
    dotfile = NamedTemporaryFile(suffix='.dot')
    dotfile.write('digraph G {\n')
    for job, dep in dependencies:
        dotfile.write('    {} -> {};\n'.format(job, dep))
    dotfile.write('}\n')
    dotfile.flush()

    return call(['dot', '-Tpng', '-o', image, dotfile.name]) == 0


def show_image(path):
    '''Show image using OS default viewer.'''
    cmd = {
        'darwin': 'open',
        'linux2': 'xdg-open',
        'win32': 'start',
    }[platform]

    return call([cmd, path]) == 0


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='Show job order in directory')
    parser.add_argument('directory', help='jobs directory [.]', default='.',
                       nargs='?')
    args = parser.parse_args(argv[1:])

    if not isdir(args.directory):
        raise SystemExit('error: {} is not a directory'.format(args.directory))

    jobfiles = glob(join(args.directory, '*.job'))
    if not jobfiles:
        raise SystemExit('error: no *.job files in {}'.format(args.directory))

    image = '/tmp/job-deps.png'
    dependencies = iter_dependencies(jobfiles)
    if not gen_image(dependencies, image):
        raise SystemExit('error: cannot run dot (PATH problem?)')

    if not show_image(image):
        raise SystemExit('error: cannot show {}'.format(image))

if __name__ == '__main__':
    main()
