#!/usr/bin/env python

from cgi import FieldStorage
from myapp import do_something_with_data

ERROR = "<html><body>Error: %s</body></html>"

def main():
    print "Content-Type: text/html"
    print

    form = FieldStorage()
    data = form.getvalue("data", "")
    key = form.getvalue("key", "").strip()
    if not (key and data):
        raise SystemExit(ERROR % "NO 'key' or 'data'")

    try:
        do_something_with_data(key, data)
    except Exception, e:
        raise SystemExit(ERROR % e)

    print "<html><body>OK</body></html>"

if __name__ == "__main__":
  main()
