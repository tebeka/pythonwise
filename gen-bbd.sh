#!/bin/bash
# Generate "Bounding Box Diagonal" image

convert \
    -size 400x400 \
    xc:skyblue \
    -fill red \
    -draw "circle 200,200 0,200" \
    -stroke black \
    -strokewidth 2 \
    -draw "line 0,0 400,400" \
    -stroke skyblue \
    -pointsize 40 \
    -draw "rotate 45 text 250,10 \"bbd\"" \
    bbd.png
