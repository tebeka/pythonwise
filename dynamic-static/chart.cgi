#!/usr/bin/env python
'''This CGI script is called by lighttpd 404 error handler when it tries to find
/charts/XXX.png.

This way the image is generated once and then we let lighttpd serve it as static
content.
'''

# The below is needed to tell pylab to work without a screen
import matplotlib; matplotlib.use("Agg")
from pylab import hist, randn, title, savefig

from os import environ
from os.path import basename
from urlparse import urlparse

def generate_chart(name, outfile):
    # Generate a random chart
    hist(randn(1000), 100)
    title("Chart for \"%s\"" % name)
    savefig(outfile)

def main():
    import cgitb; cgitb.enable()

    o = urlparse(environ.get("REQUEST_URI", ""))
    if not o.path:
        print "Content-type: text/plain\n"
        print "ERROR: Can't find path"
        raise SystemExit

    outfile = "charts/%s" % basename(o.path)
    name = basename(o.path).replace(".png", "")
    if not name:
        print "Content-type: text/plain\n"
        print "ERROR: 'name' not specified"
        raise SystemExit

    generate_chart(name, outfile)
    image = open(outfile, "rb").read()

    print "Content-type: image/png\n"
    print image

if __name__ == "__main__":
    main()

