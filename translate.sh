#!/bin/bash

# Use Google to translate from English to Hebrew

# Based on
# http://www.commandlinefu.com/commands/view/5516/google-translate

if [ $# -ne 1 ]; then
    echo "usage: $(basename $0) WORD"
    exit 1
fi

case $1 in
    -h|--help ) echo "usage $(basename $0) WORD"; exit;;
esac

url="http://ajax.googleapis.com/ajax/services/language/translate?v=1.0"
url="${url}&langpair=en|he&q=$1"
curl -s "$url" | sed 's/.*"translatedText":"\([^"]*\)".*}/\1\n/' | \
    fribidi --nopad
