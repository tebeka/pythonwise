#!/usr/bin/env python
'''Generate QR code using Google Charts API'''

import sys
# Python 3/2 compatibility
if sys.version_info[:2] < (3, 0):
    from urllib import urlopen, urlencode
    import httplib
    stdout = sys.stdout
else:
    from urllib.request import urlopen
    from urllib.parse import urlencode
    import http.client as httplib
    stdout = sys.stdout.buffer


def gen_qr(data, size):
    charts_url = 'https://chart.googleapis.com/chart'
    params = [
        ('cht', 'qr'),
        ('chs', size),
        ('chl', data),
    ]
    query = urlencode(params)
    url = '%s?%s' % (charts_url, query)
    fo = urlopen(url)
    if fo.code != httplib.OK:
        raise ValueError('bad reply from Google %d' % fo.code)
    return fo.read()


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='Generate QR using Google Charts (PNG)')
    parser.add_argument('data', help='data to encode')
    parser.add_argument('--out', '-o', help='output file name (stdin)',
                        default='-')
    parser.add_argument('--size', '-s', help='image size (200x200)',
                        default='200x200')
    args = parser.parse_args()

    try:
        img_data = gen_qr(args.data, args.size)
        out = stdout if args.out == '-' else open(args.out, 'wb')
        out.write(img_data)
    except ValueError as err:
        raise SystemExit('error: {}'.format(err))
    except IOError as err:
        raise SystemExit(
            'error: cannot open {} for writing - {}'.format(args.out, err))
