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
    # writeback=1 means storage will be updated directly, slower but easier
    return shelve.open("%s/.twittalk-seen" % expanduser("~"), writeback=1)

def get_items(fo):
    # <item><title>...</title><description>...</description><pubDate>...</pubDate>
    #       <guid>..</guid><link>...</link></item>
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

def get_new_messages(opener, seen):
    def is_new(tg):
        return tg[1] not in seen

    fo = opener.open(url)
    for title, guid in filter(is_new, get_items(fo)):
        seen[guid] = 1
        yield title

def build_ui(user, password, seen):
    import Tkinter as tk

    root = tk.Tk()
    root.title("Twittalk")
    tk.Label(root, text="User:").grid(row=0, sticky=tk.W)
    tk.Label(root, text="Password:").grid(row=1, sticky=tk.W)
    user = tk.Entry(root)
    user.grid(row=0, column=1)
    passwd = tk.Entry(root, show="*")
    passwd.grid(row=1, column=1)
    start = tk.Button(root, text="Start")
    start.grid(row=2)

    user.focus()

    root.mainloop()




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
    parser.add_option("-g", "--no-gui", help="run without GUI", 
          dest="gui", action="store_false", default=1)

    opts, args = parser.parse_args(argv[1:])
    if args:
        parser.error("wrong number of arguments") # Will exit

    seen = open_seen()
    opener = create_opener(opts.user, opts.password)
    url = "http://twitter.com/statuses/friends_timeline.rss"

    go = iter((1, 0)).next if opts.once else repeat(1).next

    def is_new(tg):
        return tg[1] not in seen

    while go():
        say_new_message()
        fo = opener.open(url)
        for title, guid in filter(is_new, get_items(fo)):
            seen[title] = 1
            say(title)

if __name__ == "__main__":
    main()
