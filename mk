#!/bin/bash
# Guess which make utility to use

# Miki Tebeka <miki.tebeka@gmail.com>

makecmd=""
if [ -f SConstruct ]; then
    makecmd="scons -Q -D"
elif [ -f build.xml ]; then
    makecmd="ant"
elif [ -f Makefile ]; then
    makecmd="make"
elif [ -f makefile ]; then
    makecmd="make"
elif [ "$OSTYPE" == "WINNT" ]; then
    proj=`ls *.dsp 2>/dev/null`
    if [ -f $proj ]; then
        makecmd="msdev $proj /MAKE"
    fi
fi

if [ -z "$makecmd" ]; then
    echo "can't find project file"
    exit 1
fi

$makecmd $@
