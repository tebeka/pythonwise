#!/bin/bash
# Test server by sending photo and viewing the output

# Image by Trish Hamme (https://flic.kr/p/cYUQv7)

if [ $# -ne 1 ]; then
    echo "error: wrong number of arguments"
    exit 1
fi

case $1 in
    -h | --help ) echo "usage: $(basename $0) edge|resize"; exit;;
    edge ) path=edge;;
    resize ) path=resize;;
    * ) echo "error: unknown operation - $1"; exit 1;;
esac

outfile=$(mktemp --suffix=.png)

curl \
    -s \
    -X POST \
    -H 'Content-Type: image/jpeg' \
    --data-binary @image.jpg \
    -o ${outfile} \
    http://localhost:8080/${path}

xdg-open ${outfile}
