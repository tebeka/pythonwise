def _build():
    from os.path import getmtime, isfile, dirname, join
    from sys import executable
    from os import system

    from setup import DYNLIB, SRC_FILE

    MODULE_DIR = dirname(__file__)

    def _run(cmd):
        return system("(cd \"%s\" && %s) > /dev/null 2>&1" % (MODULE_DIR, cmd))

    _full_src = join(MODULE_DIR, SRC_FILE)
    _full_dynlib = join(MODULE_DIR, DYNLIB)

    if (not isfile(_full_dynlib)) or (getmtime(_full_dynlib) < getmtime(_full_src)):
        assert _run("%s setup.py build_ext -i" % executable) == 0, "build error" 

_build()
del _build 
from _greet import * 
