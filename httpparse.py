#!/usr/bin/env python

# Parse HTTP response

from StringIO import StringIO
from httplib import HTTPResponse

class FakeSocket(StringIO):
    def makefile(self, *args, **kw):
        return self

def httpparse(fp):
    socket = FakeSocket(fp.read())
    response = HTTPResponse(socket)
    response.begin()

    return response

if __name__ == "__main__":
    from os import popen

    pipe = popen("curl -si http://google.com")
    response = httpparse(pipe)

    print response.getheaders()


