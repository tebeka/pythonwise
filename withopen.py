#!/usr/bin/env python3
""" "with open as X" frequency"""

from os import walk
from os.path import isdir
from collections import Counter
import re
import pandas as pd

def py_files(start):
    """Iterator return all Python files under 'start'"""
    for root, dirs, files in walk(start):
        for name in files:
            if not name.endswith('.py'):
                continue
            yield '%s/%s' % (root, name)


def py_lines(start):
    """All lines from all Python files under start"""
    for path in py_files(start):
        with open(path, encoding='latin-1') as fo:
            yield from fo


def dir_type(val):
    """Check that val points to an existing directory"""
    if not isdir(val):
        raise ValueError('%s - no such directory' % val)
    return val


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('root', help='root dir', default='.', type=dir_type,
            nargs='?')
    args = parser.parse_args()

    names = Counter()
    for line in py_lines('%s/Lib' % args.root):
        if 'with open' not in line:
            continue

        match = re.search('as (\w+):', line)
        if not match:
            continue
        names[match.group(1)] += 1


    # Use reversed to get most common on top of chart
    name, count = zip(*reversed(names.most_common()))
    df = pd.DataFrame({
        'name': name,
        'count': count,
    })

    ax = df.plot(x='name', y='count', kind='barh', fontsize=8)
    ax.figure.savefig('withopen.png')
