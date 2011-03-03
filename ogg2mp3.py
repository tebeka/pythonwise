#!/usr/bin/env python

from os import walk, remove, getpid
from time import time
from subprocess import check_call
import multiprocessing as mp

def oggs(path=None):
    "List of ogg files under current directory"
    path = path or "."
    for root, dirs, files in walk(path):
        for file in files:
            if file.endswith(".ogg"):
                yield "%s/%s" % (root, file)

def tmpwav():
    "Temporary wav file name"
    return "/tmp/%s-%s.wav" % (getpid(), int(time()))

def ogg2mp3(ogg, mp3):
    "Convert ogg to mp3 using oggdec and lame"
    tmp = tmpwav()
    print "%s --> %s" % (ogg, mp3)
    check_call(["oggdec", "-Q", "-o", tmp, ogg])
    check_call(["lame", "--quiet", tmp, mp3])

    remove(tmp)

def convert_dir(path=None):
    pool = mp.Pool(processes=4)
    results = []

    for ogg in oggs(path):
        mp3 = ogg.replace(".ogg", ".mp3")
        results.append(pool.apply_async(ogg2mp3, (ogg, mp3)))

    for result in results:
        result.wait()

def main(argv=None):
    import sys
    from optparse import OptionParser
    from os.path import isdir

    argv = argv or sys.argv

    parser = OptionParser("%prog DIRECTORY")
    opts, args = parser.parse_args(argv[1:])
    if len(args) != 1:
        parser.error("wrong number of arguments") # Will exit

    path = args[0]
    if not isdir(path):
        raise SystemExit("error: %s is not a directory" % path)

    convert_dir(path)

if __name__ == "__main__":
    main()

