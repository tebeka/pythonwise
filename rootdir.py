#!/usr/bin/env python
# If you're using Python, you can just write from root import ROOT_DIR, however
# if you're using bash you can write ROOTDIR=`./rootdir.py` and then use
# $ROOTDIR

from os import environ
from os.path import join
from getpass import getuser

if "DEBUG" in environ:
   # Every user has his/her own test root directory
   ROOT_DIR = join("/tmp", "testing", getuser())
else:
   ROOT_DIR = "/usr/local/cool"

if __name__ == "__main__":
   print ROOT_DIR
