#!/usr/bin/env python
'''Print message using ANSI terminal codes'''

__author__ = "Miki Tebeka <miki@mikitebeka.com>"

from sys import stdout, stderr

# Format
bright = 1
dim = 2
underline = 4
blink = 5
reverse = 7
hidden = 8

# Forground
black = 30
red = 31
green = 32
yellow = 33
blue = 34
magenta = 35
cyan = 36
white = 37

# Background
on_black = 40
on_red = 41
on_green = 42
on_yellow = 43
on_blue = 44
on_magenta = 45
on_cyan = 46
on_white = 47

def ansiformat(msg, *args):
    '''Format msg according to args.

    See http://www.termsys.demon.co.uk/vtansi.htm for more details/
    '''
    return "\033[%sm%s\033[0m" % (";".join(["%s" % f for f in args]), msg)

def ansiprint(msg, *args, **kw):
    '''Print formatted message.

    Should work on ANSI compatible terminal.
    '''

    if kw.get("stderr", 0):
        outfo = stderr
    else:
        outfo = stdout

    outfo.write(ansiformat(msg, *args))
    outfo.flush()

if __name__ == "__main__":
    from sys import argv, exit
    from os.path import basename

    h = {
        "bright" : bright,
        "dim" : dim,
        "underline" : underline,
        "blink" : blink,
        "reverse" : reverse,
        "hidden" : hidden,
        "black" : black,
        "red" : red,
        "green" : green,
        "yellow" : yellow,
        "blue" : blue,
        "magenta" : magenta,
        "cyan" : cyan,
        "white" : white,
        "on_black" : on_black,
        "on_red" : on_red,
        "on_green" : on_green,
        "on_yellow" : on_yellow,
        "on_blue" : on_blue,
        "on_magenta" : on_magenta,
        "on_cyan" : on_cyan,
        "on_white" : on_white
    }

    eg = "e.g. ansiprint hello red on_green underline -> %s" % \
        ansiformat("hello", red, on_green, underline)

    if len(argv) < 2:
        print >> stderr, "usage: %s message [format ...]" % basename(argv[0])
        print >> stderr, eg
        exit(1)

    for i in argv[2:]:
        if i not in h:
            ansiprint("%s: Unknown format\n" % i, red, bright, stderr=True)
            print >> stderr, "Formats can be:",
            msg = ", ".join([ansiformat(f, h[f]) for f in h.keys()])
            print msg
            print >> stderr, eg
            exit(1)

    ansiprint(argv[1], *[h[i] for i in argv[2:]])
    print
