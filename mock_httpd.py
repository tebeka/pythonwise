#!/usr/bin/env python
# Using BaseHTTPServer for mocking servers

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from time import sleep, time
from urllib import urlopen
import httplib
import re


def wait_for_server(url, timeout=5):
    '''Wait for server to become available.'''
    start = time()
    while time() - start < timeout:
        try:
            urlopen(url)
            return
        except IOError:
            sleep(0.1)

    raise ValueError('no server at {}'.format(url))


def run_server(config, port=0, ctype='application/json'):
    '''Run HTTP server, return server object.
    Config is a dictionary path -> data

    If port is 0, a random free port will be selected (you can access the port
    from server.server_port, or the base url in server.url)

    ctype is the Content-Type header returned by the server
    '''
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Normalize path
            path = re.sub('/+', '/', self.path)
            if path not in config:
                self.send_error(httplib.NOT_FOUND, self.path + ' not found')
                return

            self.send_response(httplib.OK)
            self.send_header('Content-Type', ctype)
            self.end_headers()
            self.wfile.write(config[path])

        def log_message(self, *args):
            '''Be quiet'''
            pass

    server = HTTPServer(('', port), Handler)
    server.url = 'http://localhost:{}'.format(server.server_port)
    t = Thread(target=server.serve_forever)
    t.daemon = True
    t.start()

    wait_for_server('{}/{}'.format(server.url, config.keys()[0]))

    return server


def _test():
    '''Example on how to use'''

    path, payload = '/hello', 'hello there'

    server = run_server({path: payload})
    data = urlopen('{}/{}'.format(server.url, path)).read()
    assert data == payload, '{} != {}'.format(data, payload)


if __name__ == '__main__':
    _test()
