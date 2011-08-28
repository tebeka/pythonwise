#!/usr/bin/env python
'''Generate word frequency from alice'''

import re
from collections import Counter
import json
from operator import itemgetter
from bz2 import decompress

def main():
    words = {}
    text = decompress(open('alice.txt.bz2', 'rb').read()).lower()
    c = Counter(m.group() for m in re.finditer('[a-z]{3,}', text))

    words = sorted(c.iteritems(), key=itemgetter(1), reverse=True)
    data = [{'label' : word, 'data' : count} for word, count in words]

    fo = open('data.js', 'w')
    fo.write('var data = ')
    json.dump(data, fo)
    fo.write(';')

if __name__ == '__main__':
    main()

