"""Using contextlib.closing to make sure sockets are closed"""

from contextlib import closing
from socket import socket
from urlparse import urlparse

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
        sock.sendall(request)

        def read():
            return sock.recv(1024)

        return ''.join(iter(read, ''))


if __name__ == '__main__':
    print(get('http://httpbin.org/ip'))
