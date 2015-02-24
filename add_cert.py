#!/usr/bin/env python
'''Add server certificate.

You'll need certutil tool installed, probably:
    apt-get install libnss3-tools
'''

from argparse import ArgumentParser, FileType
from subprocess import check_call, CalledProcessError
from os import environ

parser = ArgumentParser(description=__doc__)
parser.add_argument('name', help='certificate name (pick one :)')
parser.add_argument('file', help='certificate file', type=FileType())
args = parser.parse_args()

cmd = [
    'certutil',
    '-d', 'sql:%s/.pki/nssdb' % environ['HOME'],
    '-A', '-t', 'P,,',
    '-n', args.name,
    '-i', args.file.name,
]

try:
    check_call(cmd)
except CalledProcessError as err:
    raise SystemExit('error: %s' % err)
