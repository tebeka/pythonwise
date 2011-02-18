#!/bin/bash
# Check files with pyflakes

export PYTHONPATH="$(./pypath.sh)"

if [ $# -eq 0 ]; then
    files=*.py
else
    files=$@
fi

/opt/python2.5/bin/pyflakes $files
