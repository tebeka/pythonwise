#!/usr/bin/env python
'''Add a URL to (or just open) Google bookmarks.'''

from HTMLParser import HTMLParser
from urllib import urlopen, urlencode
import webbrowser


class TitleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.title = ''
        self.in_title = False

    def is_title(self, tag):
        return tag.lower() == 'title'

    def handle_starttag(self, tag, attrs):
        if self.is_title(tag):
            self.in_title = True

    def handle_endtag(self, tag):
        if self.is_title(tag):
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def get_title(url):
    try:
        req = urlopen(url)
        if req.code >= 400:
            raise IOError('bad return code - {}'.format(req.code))

        parser = TitleParser()
        parser.feed(req.read())
        return parser.title
    except IOError as err:
        print('warning: cannot get {} data - {}'.format(url, err))
        return ''


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='Google Bookmark')
    parser.add_argument('url', nargs='?', help='URL to bookmark')
    args = parser.parse_args(argv[1:])

    url = 'https://www.google.com/bookmarks/mark'
    query = {'op': 'edit'}

    if args.url:
        query['bkmk'] = args.url
        query['title'] = get_title(args.url)

    url = '{}?{}'.format(url, urlencode(query))
    webbrowser.open(url)


if __name__ == '__main__':
    main()
