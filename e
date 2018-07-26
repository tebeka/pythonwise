#!/usr/bin/env python
"""Run nvim in new terminal window"""

from subprocess import Popen
from sys import argv
from shlex import quote

cmd = [
    'xfce4-terminal',
    '-T', 'nvim',
    '-e', ' '.join(['nvim'] + [quote(arg) for arg in argv[1:]])
]
Popen(cmd)
