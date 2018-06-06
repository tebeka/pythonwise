#!/usr/bin/env python
"""History statistics"""

import shlex
from argparse import ArgumentParser
from datetime import datetime
from os.path import expanduser
import pandas as pd


def parse_line(line):
    """Parse a history line, return None if can't"""
    #: 1523386209:0;convert -crop 600x400 raw/01-add.png 01-add.png
    try:
        line = line.decode('utf-8')
    except UnicodeDecodeError:
        return None

    line = line[2:]  # Remove ': ' prefix

    fields = line.split(';', maxsplit=1)
    if len(fields) != 2:
        return None

    try:
        command = shlex.split(fields[1])
    except ValueError:
        command = fields[1].split()

    ts, _ = fields[0].split(':')
    return {
        'time': datetime.fromtimestamp(int(ts)),
        'command': command[0],
        'nargs': len(command[1:]),
    }


def load_history(file_name):
    """Return DataFrame from history file"""
    with open(file_name, 'rb') as fp:
        records = filter(None, (parse_line(line) for line in fp))
        return pd.DataFrame.from_records(records)


parser = ArgumentParser(description=__doc__)
parser.add_argument(
    '--count', help='number of items to show', default=20, type=int)
args = parser.parse_args()

histfile = expanduser('~/.zsh_history')
df = load_history(histfile)
vc = df['command'].value_counts()
print(vc[:args.count])
