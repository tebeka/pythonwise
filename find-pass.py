#!/usr/bin/env python

from subprocess import check_output, STDOUT, CalledProcessError
from sys import platform
import re

# password: "XXXXX"
find_passwd = re.compile('password: "([^"]+)"').search
#     "acct"<blob>="miki.tebeka@gmail.com"
find_user = re.compile('"acct"<blob>="([^"]+)"').search


def find_key(fn, out):
    match = fn(out)
    return match and match.group(1)


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='')
    parser.add_argument('domain')
    args = parser.parse_args(argv[1:])

    if platform != 'darwin':
        raise SystemExit('error: {} works only on OSX'.format(parser.prog))

    domain = args.domain

    cmd = [
        'security',
        'find-internet-password',
        '-g',
        '-s', domain,
    ]
    try:
        out = check_output(cmd, stderr=STDOUT)
    except CalledProcessError:
        raise SystemExit('error: not password for {}'.format(domain))

    user = find_key(find_user, out)
    if not user:
        raise SystemExit('error: cannot find user for {}'.format(domain))
    print(user)

    passwd = find_key(find_passwd, out)
    if not passwd:
        raise SystemExit('error: cannot find password for {}'.format(domain))
    print(passwd)


if __name__ == '__main__':
    main()
