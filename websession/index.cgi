#!/usr/bin/env python

from websession import WebSession

session = WebSession()

key = "key"
old = session.get(key, 0)
new = old + 1
session[key] = new

print session.cookie
print "Content-Type: text/html"
print

print "<html><body>"
print "<pre>"
print "session id: %s" % session.id
print "old: %s" % old
print "new: %s" % new
print "</pre>"
print "</body></html>"

session.save()
