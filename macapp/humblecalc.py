#!/usr/bin/env python
# Very humble calculator, written as "Web Desktop Application"

__author__ = "Miki Tebeka <miki.tebeka@gmail.com>"

from __future__ import division
from math import *
from operator import isNumberType

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from urlparse import urlparse
from cgi import parse_qs
import httplib

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        o = urlparse(self.path)
        if o.path == "/eval":
            self.eval(o.query)
        elif o.path == "/quit":
            self.end_headers()
            self.wfile.write("Bye")
            self.wfile.flush()
            # self.server.shutdown() hangs, so we do it the brutal way
            import os; os._exit(0)
        else:
            SimpleHTTPRequestHandler.do_GET(self)

    def eval(self, query):
        q = parse_qs(query)
        expr = q.get("expr", [""])[0]
        try:
            # FIXME: Never do this on production, this is a huge security risk
            result = str(eval(expr))
        except Exception, e:
            result = "ERROR"

        self.send_response(httplib.OK)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(result)

if __name__ == "__main__":
    import webbrowser
    port = 8822
    server = HTTPServer(("", port), RequestHandler)
    webbrowser.open("http://localhost:%s" % port)
    server.serve_forever()
