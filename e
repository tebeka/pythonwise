#!/usr/bin/env python
"""Run nvim in new terminal window"""

from subprocess import Popen
from sys import argv

cmd = [
    'xfce4-terminal',
    '-T', 'nvim',
    '-e', ' '.join(['nvim'] + argv[1:])
]
Popen(cmd)
