#!/usr/bin/env python
'''Get content of "foreign" web pages, enable cross-site AJAX'''

from urllib2 import urlopen, URLError
from cgi import FieldStorage

if __name__ == "__main__":
    import cgitb; cgitb.enable()

    form = FieldStorage()
    url = form.getvalue("url", "")
    if not url:
        raise SystemExit("no url")

    try:
        o = urlopen(url)
    except (URLError, ValueError), e:
        raise SystemExit("error: %s" % e)

    print "Content-type: %(content-type)s\n" % o.headers
    print o.read()
