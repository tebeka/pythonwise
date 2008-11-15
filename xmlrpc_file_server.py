#!/usr/bin/env python
'''Simple file client/server using XML RPC'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import ServerProxy, Error as XMLRPCError
import socket

def get_file(filename):
  fo = open(filename, "rb")
  try: # When will "with" be here?
      return fo.read()
  finally:
      fo.close()

def main(argv=None):
  if argv is None:
      import sys
      argv = sys.argv

  default_port = "3030"
  from optparse import OptionParser

  parser = OptionParser("usage: %prog [options] [[HOST:]PORT]")
  parser.add_option("--get", help="get file", dest="filename",
          action="store", default="")

  opts, args = parser.parse_args(argv[1:])
  if len(args) not in (0, 1):
      parser.error("wrong number of arguments") # Will exit

  if args:
      port = args[0]
  else:
      port = default_port

  if ":" in port:
      host, port = port.split(":")
  else:
      host = "localhost"

  try:
      port = int(port)
  except ValueError:
      raise SystemExit("error: bad port - %s" % port)

  if opts.filename:
      try:
          proxy = ServerProxy("http://%s:%s" % (host, port))
          print proxy.get_file(opts.filename)
          raise SystemExit
      except XMLRPCError, e:
          error = "error: can't get %s (%s)" % (opts.filename, e.faultString)
          raise SystemExit(error)
      except socket.error, e:
          raise SystemExit("error: can't connect (%s)" % e)

  server = SimpleXMLRPCServer(("localhost", port))
  server.register_function(get_file)
  print "Serving files on port %d" % port
  server.serve_forever()

if __name__ == "__main__":
  main()
