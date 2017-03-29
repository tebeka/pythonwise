#!/bin/bash
# Color log lines according to level

case $1 in
    -h | --help ) echo "usage: $(basename $0)"; exit;;
esac

if [ $# -ne 0 ]; then
    2>&1 echo "error: wrong number of arguments"
    exit 1
fi

awk '
    /INFO/ {print "\033[32m" $0 "\033[39m"; next}
    /WARNING/ {print "\033[33m" $0 "\033[39m"; next}
    /CRITICAL/ {print "\033[31m" $0 "\033[39m"; next}
    /FATAL/ {print "\033[31m" "\033[1m" $0 "\033[0m" "\033[39m"; next}
    // {print $0}
'
