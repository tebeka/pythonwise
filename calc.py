#!/usr/bin/env python
'''Small calculator'''

from __future__ import division # Detault to real devision
from math import * # Get all math goodies in global namespace
from optparse import OptionParser

USAGE = '''usage: %prog [options] MATH_EXPRESSION
    e.g. calc '7 * 29' -> 203
'''

def show_gui(text=""):
    import Tkinter as tk
    from operator import isNumberType

    root = tk.Tk()
    root.option_add("*font", "Courier -40 bold")
    root.bind("<Escape>", lambda e: root.quit())
    expr = tk.Entry(root, width=40)
    expr.insert(0, text)
    expr.pack(side=tk.LEFT)
    tk.Label(root, text="=").pack(side=tk.LEFT)
    answer = tk.Label(root)
    answer.pack(side=tk.LEFT)
    expr.focus()

    def poll():
        s = expr.get()
        try:
            ans = eval(expr.get())
            if isNumberType(ans):
                answer["text"] = str(eval(s))
        except Exception, e:
            pass
        root.after(100, poll)


    poll()
    root.mainloop()

def main(argv=None):
    if argv is None:
        import sys
        argv = sys.argv

    from optparse import OptionParser

    parser = OptionParser(USAGE.strip())
    parser.add_option("-g", "--gui", help="run in gui mode", 
        dest="gui", action="store_true", default=0)

    opts, args = parser.parse_args(argv[1:])

    nargs = (0, 1) if opts.gui else (1, )
    if len(args) not in nargs:
        parser.error("wrong number of arguments") # Will exit

    if opts.gui:
        text = args[0] if args else ""
        show_gui(text)
    else:
        try:
            print eval(args[0])
        except Exception, e:
            raise SystemExit("error: %s" % e)

if __name__ == "__main__":
    main()
