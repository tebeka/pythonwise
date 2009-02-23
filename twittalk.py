#!/usr/bin/env python
# Hear Twitter talking (idea from http://tinyurl.com/dl4pr2)

from urllib2 import HTTPPasswordMgrWithDefaultRealm, \
                    HTTPBasicAuthHandler, build_opener
import shelve
from os.path import expanduser
from xml.etree.cElementTree import parse as parse_xml
from subprocess import Popen, PIPE

def create_opener(user, password):
    passwd_mgr = HTTPPasswordMgrWithDefaultRealm()
    passwd_mgr.add_password(None, "http://twitter.com", user, password)
    handler = HTTPBasicAuthHandler(passwd_mgr)
    return build_opener(handler)

def open_seen():
    return shelve.open("%s/.twittalk-seen" % expanduser("~"), writeback=1)

def get_items(fo):
    def func(item):
        return map(item.findtext, ("title", "guid"))

    return map(func, parse_xml(fo).findall("//item"))

def tts(text):
    pipe = Popen(["festival", "--tts"], stdin=PIPE)
    print >> pipe.stdin, text
    pipe.stdin.close()
    pipe.wait()

def say(text):
    # We do this to let you focus on the new text, very much like the 
    # "ding dong" sound in many PA system
    tts("New Twitt") 
    tts(text)

def main(argv=None):
    if argv is None:
        import sys
        argv = sys.argv

    from time import sleep
    from itertools import repeat
    from optparse import OptionParser

    parser = OptionParser("%prog")
    parser.add_option("-1", "--once", help="run one time", dest="once",
            default=0, action="store_true")
    parser.add_option("-u", "--user", help="user name", dest="user",
            default="bugs_bunny")
    parser.add_option("-p", "--password", help="password", dest="password",
            default="whats_up_doc")
    opts, args = parser.parse_args(argv[1:])
    if args:
        parser.error("wrong number of arguments") # Will exit

    seen = open_seen()
    opener = create_opener(opts.user, opts.password)
    url = "http://twitter.com/statuses/friends_timeline.rss"

    go = iter((1, 0)).next if opts.once else repeat(1).next

    while go():
        fo = opener.open(url)
        for title, guid in get_items(fo):
            if title in seen:
                continue
            seen[title] = 1
            say(title)

if __name__ == "__main__":
    main()
