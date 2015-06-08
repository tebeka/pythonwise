"""Using contextlib.closing to make sure sockets are closed"""

from contextlib import closing
from functools import partial
from socket import socket

import sys

if sys.version_info[:2] < (3, 0):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

request_template = '''\
GET %s HTTP/1.1
Host: %s
Connection: close

'''


def get(url):
    """Get web page from URL using "raw" sockets"""
    url = urlparse(url)

    request = request_template % (url.path, url.netloc)
    sock = socket()
    with closing(sock):
        sock.connect((url.netloc, 80))
        sock.sendall(request.encode('utf-8'))
        data = b''.join(iter(partial(sock.recv, 1024), b''))
        return data


if __name__ == '__main__':
    data = get('http://httpbin.org/ip')
    print(data.decode('utf-8'))
