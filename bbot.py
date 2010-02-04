#!/usr/bin/env python
# Watch builds on buildbot and publish to twitter

from time import time, sleep
from xmlrpclib import ServerProxy
from subprocess import call
from urllib import urlopen

user, password = "tebeka", "SECRET_PASSWORD"
bbot_url = "http://buildbot.example.com/xmlrpc"
tweet_url = "http://%s:%s@twitter.com/statuses/update.xml" % (user, password)

def main():
    proxy = ServerProxy(bbot_url)
    last_time = time()

    while 1:
        now = time()
        builds = proxy.getAllBuildsInInterval(last_time, now)
        for build in builds:
            builder, build, status = build[0], build[1], build[5]
            status = "OK" if status == "success" else "BROKEN"
            message = "[%s] build %s is %s" % (builder, build, status)
            urlopen(tweet_url, "status=%s" % message)

        last_time = now if builds else last_time
        sleep(10)

if __name__ == "__main__":
    main()
