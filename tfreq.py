#!/usr/bin/env python2
'''Show user twitter post frequency.

You'll need you twitter credientials (from
https://dev.twitter.com/apps/<app-id>/show in ~/.twitter

~/.twitter should be in the following format (JSON)

    {
        "token": "<access token>",
        "token_secret": "<access token secert>",
        "consumer_key": "<consumer key>",
        "consumer_secret": "<consumer secret>"
    }
'''

from twitter import OAuth, Twitter

from collections import Counter
from datetime import datetime, timedelta
from os.path import expanduser, isfile
import json
import re


auth_file = expanduser('~/.twitter')


def parse_time(value):
    # Sat Apr 21 10:38:38 +0000 2012
    value = re.sub(' [+-]\d{4} ', ' ', value)  # Remove timezone
    return datetime.strptime(value, '%a %b %d %H:%M:%S %Y')


def load_auth(filename):
    with open(filename) as fo:
        return json.load(fo)


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='Show user twitter frequency')
    parser.add_argument('user', help='twitter user name')
    args = parser.parse_args(argv[1:])

    if not isfile(auth_file):
        raise SystemExit('error: cannot find auth file {}'.format(auth_file))

    auth_opts = load_auth(auth_file)
    twitter = Twitter(auth=OAuth(**auth_opts))
    posts = twitter.statuses.user_timeline(screen_name=args.user, count=200)

    by_day = Counter(parse_time(post['created_at']).date() for post in posts)

    # Fill missing days with zeros
    start, end = min(by_day.keys()), max(by_day.keys())
    day = timedelta(days=1)
    current = start + day
    while current < end:
        if current not in by_day:
            by_day[current] = 0
        current += day

    freqs = sorted(by_day.values())
    print('sample size: {} ({} -> {})'.format(len(freqs), start, end))
    print('average: {:.02f}/day'.format(sum(freqs) / float(len(freqs))))
    print('median: {}/day'.format(freqs[len(freqs)/2]))
    print('max: {}'.format(max(freqs)))


if __name__ == '__main__':
    main()
