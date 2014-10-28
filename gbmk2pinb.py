#!/usr/bin/env python
'''
Port Google Bookmarks over to pinboard.in
* Export Google Bookmarks by hitting
    http://www.google.com/bookmarks/?output=xml&num=10000
* Get pinboard auth_token from https://pinboard.in/settings/password

Run:
    ./gbmk2pinb.py bookmarks.xml --auth-token <token>
'''
import requests

from cStringIO import StringIO
from datetime import datetime
import httplib
import logging as log
import xml.etree.cElementTree as et

add_url = 'https://api.pinboard.in/v1/posts/add'

# Example XML:
# <xml_api_reply version="1">
#   <bookmarks>
#     <bookmark>
#       <title>Finnish Doctors Are Prescribing Video Games For ADHD -
#       Slashdot</title>
#       <url>bit.ly/15J6NSBCustomize</url>
#       <timestamp>1381590052580408</timestamp>
#       <id>536897562302183779</id>
#       <labels>
#         <label>psychology</label>
#         <label>adhd</label>
#         <label>video</label>
#         <label>games</label>
#       </labels>
#     </bookmark>
#   ...

def iter_xml(fo):
    tree = et.parse(fo)
    for bmk in tree.iterfind('.//bookmark'):
        title = bmk.find('title')
        ts = int(bmk.find('timestamp').text)
        yield {
            'title': title.text if title is not None else 'UNKNOWN TITLE',
            'url': bmk.find('url').text,
            'labels': [elem.text for elem in bmk.iterfind('.//label')],
            'timestamp': datetime.utcfromtimestamp(ts/1000000),
        }


def bmk2params(bmk, auth_token):
    return {
        'url': bmk['url'],
        'description': bmk['title'],
        'tags': ','.join(bmk['labels']),
        'dt': bmk['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ'),
        'auth_token': auth_token,
        'replace': 'yes',
    }


def parse_reply(reply):
    if reply.status_code != httplib.OK:
        return False

    root = et.parse(StringIO(reply.content)).getroot()
    code = root.get('code')
    if code != 'done':
        log.error(code)
        return False

    return True


def post_bookmark(bmk, auth_token):
    params = bmk2params(bmk, auth_token)

    reply = requests.post(add_url, params=params)
    return parse_reply(reply)


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='Post Google Bookmarks to Pinboard')
    parser.add_argument('filename')
    parser.add_argument('--auth-token')
    parser.add_argument('--start', help='start offset', type=int, default=0)
    args = parser.parse_args(argv[1:])

    with open(args.filename) as fo:
        bmks = list(iter_xml(fo))

    if args.start > 0:
        bmks = bmks[args.start:]

    for i, bmk in enumerate(bmks):
        print(u'{}: {}'.format(args.start + i, bmk['title']))
        if not post_bookmark(bmk, args.auth_token):
            raise SystemExit('error: cannot post {}'.format(bmk['title']))


if __name__ == '__main__':
    main()
