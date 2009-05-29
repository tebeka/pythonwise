#!/usr/bin/env python
'''Simple web based phone book'''

__author__ = "Miki Tebeka <miki.tebeka@gmail.com>"

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from urlparse import urlparse
from cgi import parse_qs
import socket

# In memory phonebook, an application will have a "real" datebase
# (I use a text file ;)
PHONES = [
    "Duffy Duck  : 1",
    "Bugs Bunny  : 2",
    "Taz         : 3",
    "Pepe Le Pew : 4",
    "Tweety Bird : 5",
    "Sylverster  : 6",
    "Elmer Fudd  : 7",
]

# We're using SimpleHTTPRequestHandler so that files will be served
# automagically
class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        o = urlparse(self.path)
        if o.path == "/search":
            self.search(o.query)
        else:
            SimpleHTTPRequestHandler.do_GET(self)

    def search(self, query):
        query = parse_qs(query)
        query = query["query"][0].lower()

        results = filter(lambda name: query in name.lower(), PHONES)
        text = "<br />\n".join(results) or "NO RESULTS FOUND!"
        self.wfile.write("<p>%s</p>" % text)

def main():
    import webbrowser
    from os import fork

    port = 8421

    # fork to make program exit after opening the browser page
    pid = fork()
    if pid:
        webbrowser.open("http://localhost:%s" % port)
    else:
        try:
            server = HTTPServer(("", port), RequestHandler)
            server.serve_forever()
        except socket.error:
            # Assume already running, we've opened the web page - enough
            pass

if __name__ == "__main__":
    main()
