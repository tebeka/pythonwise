#!/usr/bin/env python

import feedparser
from cgi import FieldStorage, escape
from time import ctime

ENTRY_TEMPLATE = '''
<a href="%(link)s"
 onmouseover="$('#%(eid)s').show();"
 onmouseout="$('#%(eid)s').hide();"
 target="_new"
>
%(title)s
</a> <br />
<div class="summary" id="%(eid)s">
%(summary)s
</div>
'''

def main():
 print "Content-type: text/html\n"

 form = FieldStorage()
 url = form.getvalue("url", "")
 if not url:
     raise SystemExit("error: not url given")

 feed = feedparser.parse(url)
 for enum, entry in enumerate(feed.entries):
     entry.eid = "entry%d" % enum
     try:
         html = ENTRY_TEMPLATE % entry
         print html
     except Exception, e:
         # FIXME: Log errors
         pass

 print "<br />%s" % ctime()

if __name__ == "__main__":
 main()

