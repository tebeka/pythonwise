#!/usr/bin/env python
'''Small calculator'''

# ======================================================#
# Copyright (c) Miki Tebeka <miki.tebeka@gmail.com>     #
# This file is under the GNU Public License (GPL), see  #
# http://www.gnu.org/copyleft/gpl.html for more details #
# ======================================================#

from __future__ import division # Detault to real devision
from math import * # Get all math goodies in global namespace
from optparse import OptionParser

description = 'Calculate math expression (e.g. calc \'7 * 29\' -> 203)'

def show_gui(text=''):
    import Tkinter as tk
    from operator import isNumberType

    root = tk.Tk()
    root.option_add('*font', 'Courier -40 bold')
    root.bind('<Escape>', lambda e: root.quit())
    expr = tk.Entry(root, width=40)
    expr.insert(0, text)
    expr.pack(side=tk.LEFT)
    tk.Label(root, text='=').pack(side=tk.LEFT)
    answer = tk.Label(root)
    answer.pack(side=tk.LEFT)
    expr.focus()

    def poll():
        s = expr.get()
        try:
            ans = eval(expr.get())
            if isNumberType(ans):
                answer['text'] = str(eval(s))
        except Exception, e:
            answer['text'] = '???'
        root.after(100, poll)

    poll()
    root.mainloop()

def main(argv=None):
    if argv is None:
        import sys
        argv = sys.argv

    from argparse import ArgumentParser


    parser = ArgumentParser(description=description)
    parser.add_argument('expression', help='math expression', default='',
                       nargs='?')
    parser.add_argument('-g', '--gui', help='run in gui mode',
        dest='gui', action='store_true', default=False)

    args = parser.parse_args(argv[1:])

    args.gui = (not sys.stdout.isatty()) or args.gui

    if args.gui:
        show_gui(args.expression)
    else:
        try:
            print(eval(args.expression or '0'))
        except Exception as e:
            raise SystemExit('error: {0}'.format(e))

if __name__ == '__main__':
    main()
