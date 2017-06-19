#!/usr/bin/env python
"""Find owner of file/directory by git commit logs"""

from argparse import ArgumentParser
from collections import Counter
from datetime import datetime
from os import path
from subprocess import check_output, CalledProcessError


def path_type(val):
    """Check that val is an existing path"""
    if not path.exists(val):
        raise ValueError('{!r} does not exists'.format(val))
    return val


def dt2str(dt):
    """Convert datetime.timedelta to human readable format"""
    if dt.days:
        return '{}D'.format(dt.days)
    if dt.seconds > 3600:
        return '{}H'.format(dt.seconds // 3600)
    return '{}M'.format(dt.seconds // 60)


parser = ArgumentParser(description=__doc__)
parser.add_argument(
    'path', help='file/directory to check', type=path_type, default='.',
    nargs='?')
count = 3
parser.add_argument(
    '--count', help='how many people to show ({})'.format(count),
    type=int, default=count)

args = parser.parse_args()

try:
    out = check_output(['git', 'log', '--format=%aN -- %aD', args.path])
except CalledProcessError as err:
    raise SystemExit('error: {}'.format(err))

commits = Counter()
# Last people who touched the code
last = []

now = datetime.utcnow()
for line in out.decode().splitlines():
    name, time = line.strip().split(' -- ')
    if len(last) < args.count and name not in last:
        # 'Tue, 6 Jun 2017 22:13:36 -0400'
        time = datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %z')
        # Convert to naive datetime so we can subtract
        time = (time - time.utcoffset()).replace(tzinfo=None)
        last.append('{} ({})'.format(name, dt2str(now-time)))
    commits[name] += 1

total = sum(commits.values())
most = []
for name, count in commits.most_common(args.count):
    perc = float(count) / total * 100
    most.append('{} ({:.1f}%)'.format(name, perc))

print('Most: {}'.format(', '.join(most)))
print('Last: {}'.format(', '.join(last)))
