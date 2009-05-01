#!/usr/bin/env python
'''Push changes in subversion repository to IRC channel'''

from twisted.words.protocols import irc
from twisted.internet.protocol import ReconnectingClientFactory
import re
from subprocess import Popen, PIPE
from xml.etree.cElementTree import parse as xmlparse
from cStringIO import StringIO

class IRCClient(irc.IRCClient):
    nickname = "svnbot"
    realname = "Subversion Bot"
    channel = "#dev"

    instance = None # Running instance

    def signedOn(self):
        IRCClient.instance = self
        self.join(self.channel)

    def svn(self, revision, author, comment):
        comment = (comment[:57] + "...") if  len(comment) > 60 else comment
        message = "SVN revision %s by %s: %s" % (revision, author, comment)
        self.say(self.channel, message)


class SVNPoller:
    def __init__(self, root, user, password):
        self.pre = ["svn", "--xml", "--username", user, "--password", password]
        self.root = root
        self.last_revision = self.get_last_revision()

    def check(self):
        if not IRCClient.instance:
            return

        try:
            last_revision = self.get_last_revision()
            if (not last_revision) or (last_revision == self.last_revision):
                return

            for rev in range(self.last_revision + 1, last_revision + 1):
                author, comment = self.revision_info(rev)
                IRCClient.instance.svn(rev, author, comment)
            self.last_revision = last_revision
        except Exception, e:
            print "ERROR: %s" % e

    def svn(self, *cmd):
        pipe = Popen(self.pre +  list(cmd) + [self.root], stdout=PIPE)
        try:
            data = pipe.stdout.read()
        except IOError: # FIXME: Find why
            data = ""
        return xmlparse(StringIO(data))

    def get_last_revision(self):
        tree = self.svn("info")
        revision = tree.find("//commit").get("revision")
        return int(revision)

    def revision_info(self, revision):
        tree = self.svn("log", "-r", str(revision))
        author = tree.find("//author").text
        comment = tree.find("//msg").text

        return author, comment

if __name__ == "__main__":
    from twisted.internet import reactor
    from twisted.internet.task import LoopingCall

    factory = ReconnectingClientFactory()
    factory.protocol = IRCClient
    #reactor.connectTCP("irc.mycompany.com", 6667, factory)
    reactor.connectTCP("localhost", 6667, factory)

    #poller = SVNPoller("http://svn.mycompany.com", "bugs", "carrot")
    poller = SVNPoller("file:///tmp/s", "bugs", "carrot")
    task = LoopingCall(poller.check)
    task.start(1)

    reactor.run()

