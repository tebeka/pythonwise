#!/usr/bin/env python
# Search the documents in Journal of Machine Learning.

import webbrowser
from urllib import urlencode

def jmlr(words):
    query = "site:http://jmlr.csail.mit.edu filetype:pdf " + " ".join(words)
    url = "http://www.google.com/search?" + urlencode([("q", query)])

    webbrowser.open(url)

if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser("usage: %prog WORD1 [WORD2 ...]")

    opts, args = parser.parse_args()
    if not args:
        parser.error("wrong number of arguments") # Will exit

    jmlr(args)
