#!/usr/bin/env python
'''Show twitter user post frequency.'''

import json
from urllib import urlopen, urlencode
from datetime import datetime, timedelta
import re
from collections import defaultdict

base = 'https://api.twitter.com/1'  # Base Twitter API url


def name2id(user_name):
    '''Convert twitter user name to user id.'''
    url = '{}/users/lookup.json?screen_name={}'.format(base, user_name)
    reply = json.load(urlopen(url))
    return reply[0]['id']


def parse_time(value):
    '''Parser twitter post time to a datetime object.'''
    # Sat Apr 21 10:38:38 +0000 2012
    value = re.sub(' [+-]\d{4} ', ' ', value)  # Remove timezone
    return datetime.strptime(value, '%a %b %d %H:%M:%S %Y')


def post_times(user_id):
    '''Post times for user.'''
    args = {
        'user_id': user_id,
        'count': '200'  # Max allowed by twitter API
    }
    url = '{}/statuses/user_timeline.json?{}'.format(base, urlencode(args))
    posts = json.load(urlopen(url))
    for post in posts:
        yield parse_time(post['created_at'])


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='')
    parser.add_argument('user', help='twitter user name')
    args = parser.parse_args(argv[1:])

    user_id = name2id(args.user)

    # Store count per day
    by_day = defaultdict(int)
    for time in post_times(user_id):
        by_day[time.date()] += 1

    # Fill missing days with zeros
    start, end = min(by_day.keys()), max(by_day.keys())
    day = timedelta(days=1)
    current = start + day
    while current < end:
        if current not in by_day:
            by_day[current] = 0
        current += day

    # Print statistics
    freqs = sorted(by_day.values())
    print('sample size: {} ({} -> {})'.format(len(freqs), start, end))
    print('average: {:.02f}/day'.format(sum(freqs) / float(len(freqs))))
    print('median: {}/day'.format(freqs[len(freqs) / 2]))
    print('max: {}'.format(max(freqs)))


if __name__ == '__main__':
    main()
