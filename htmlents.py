#!/usr/bin/env python

from urllib import urlopen
import re
import webbrowser

W3_URL = "http://www.w3.org/TR/WD-html40-970708/sgml/entities.html"
FILE_NAME = "/tmp/html-entities.html"
find_entity = re.compile("!ENTITY\s+([A-Za-z][A-Za-z0-9]+)").search

fo = open(FILE_NAME, "wt")

print >> fo, "<html><body><table border=\"1\">"

for line in urlopen(W3_URL):
    match = find_entity(line)
    if match:
        entity = match.groups()[0]
        print >> fo, "<tr><td>%s</td><td>&%s;</td></tr>" % (entity, entity)
print >> fo, "</table></body></html>"
fo.close()

webbrowser.open(FILE_NAME)
