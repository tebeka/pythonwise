#!/usr/bin/env python
'''A "backdoor" shell for running servers (very much like Twisted manhole).

This one uses only modules found in the standard library.
'''

from SocketServer import StreamRequestHandler, TCPServer, ThreadingMixIn
from threading import Thread
from traceback import print_exc

EOF = chr(4)

class PyHandler(StreamRequestHandler):

    def handle(self):
        env = self.env.copy()
        self.wfile.write("Welcome to backdoor (type 'exit()' to exit)")
        while True:
            try:
                self.wfile.write(">>> ")
                expr = self.rfile.readline().rstrip()
                if expr == EOF:
                    return
                try:
                    value = eval(expr, globals(), env)
                    self.wfile.write(format(value) + "\n")
                except:
                    exec expr in env
            except (EOFError, SystemExit):
                return
            except Exception as e:
                print_exc(file=self.wfile)

class ThreadedServer(ThreadingMixIn, TCPServer):
    daemon_threads = True

def server_thread(env, port):
    class Handler(PyHandler):
        env = env
    server = ThreadedServer(("localhost", port), Handler)
    server.serve_forever()

DEFAULT_PORT = 9998
def serve(env, port=DEFAULT_PORT):
    t = Thread(target=server_thread, args=(env, port))
    t.daemon = True
    t.start()

    return t

if __name__ == "__main__":
    env = {"a" : 1}
    t = serve(env)
    t.join()
