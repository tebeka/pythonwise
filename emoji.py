#!/usr/bin/env python
'''Find an emoji'''

# You can generate ~/.emoji with the following command
# lynx -dump http://www.emoji-cheat-sheet.com/ | egrep -o ':[^:]+:' > ~/.emoji

from os.path import expanduser, isfile
import matplotlib.pyplot as plt
import re
import sys

if sys.version_info[0] > 2:
    from urllib.request import urlopen
else:
    from urllib import urlopen


def show_emoji(name):
    img = name[1:-1]  # :ship: -> ship
    url = 'http://www.emoji-cheat-sheet.com/graphics/emojis/{}.png'.format(img)
    fo = urlopen(url)
    img = plt.imread(fo)
    plt.imshow(img)
    plt.show()


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='Show emoji')
    parser.add_argument('query', help='query string', nargs='?')
    parser.add_argument('--show', '-s', help='show images',
                        action='store_true', default=False)
    args = parser.parse_args(argv[1:])

    filename = expanduser('~/.emoji')
    if not isfile(filename):
        raise SystemExit('error: cannot find {}'.format(filename))

    with open(filename) as fo:
        data = fo.read()

    regexp = ':.*{}.*:'.format(args.query or '')
    for match in re.findall(regexp, data):
        print(match)
        if args.show:
            show_emoji(match)


if __name__ == '__main__':
    main()
