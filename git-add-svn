#!/usr/bin/env python

# Add subversion repsotory to a git one
# Run (at top of svn repository)
#   git init
#   git-add-svn
#   git ci -a -m "Initial import from svn $(svn info | grep Revision)"

__author__ = "Miki Tebeka <miki@mikitebeka.com>"

from os import walk
from os.path import join
from fnmatch import fnmatch
from itertools import ifilter
from subprocess import call
from sys import stdout
import re

is_vcs = re.compile("\.(git|svn)", re.I).search

def make_pred(exclude):
    def is_ok(name):
        return not any((fnmatch(name, ext) for ext in exclude))
    return is_ok

def all_files():
    for root, dirs, files in walk("."):
        if is_vcs(root):
            continue
        for name in files:
            yield join(root, name)

def git_add_svn(exclude):
    pred = make_pred(exclude)
    for filename in ifilter(pred, all_files()):
        print filename
        stdout.flush()
        call(["git", "add", "-f", filename])

def main(argv=None):
    import sys
    from optparse import OptionParser

    argv = argv or sys.argv

    parser = OptionParser("%prog [options]")
    parser.add_option("-e", "--exclude", dest="exclude", action="append",
            help="extension to exclude")

    opts, args = parser.parse_args(argv[1:])
    if args:
        parser.error("wrong number of arguments") # Will exit

    git_add_svn(opts.exclude or [])


if __name__ == "__main__":
    main()
