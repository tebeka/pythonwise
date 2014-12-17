#!/bin/bash
# Utility script that print PYTHONPATH for working with AppEngine

root="/opt/google_appengine"
pypath=""
for dir in ${root}/lib/*; do
    inner="${dir}/lib"
    if [ -d "$inner" ]; then
        pypath="${pypath}${inner}:"
    else
        pypath="${pypath}${dir}:"
    fi
done

echo "${root}:${pypath}:${PYTHONPATH}"
