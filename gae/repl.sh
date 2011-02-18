#!/bin/bash
# Run ipython repl (in a new gnome terminal) with right PYTHONPATH for AppEngine

export PYTHONPATH="$(./pypath.sh)"

# GUI mode
if [ "$1" != "--no-fork" ]; then
    gnome-terminal -t '*PYTHON*' -x $0 --no-fork $*&
    exit
fi

shift
/opt/python2.5/bin/ipython
