from uuid import uuid4
from Cookie import SimpleCookie
from os import environ, mkdir
from cPickle import load, dump, PickleError 
from os.path import isfile, isdir
import atexit

class WebSession(dict):

    COOKIE_NAME = "my-cookie-name"
    SESSIONS_DIR = "/tmp/web-sessions"

    def __init__(self):
        self.cookie = self.session_cookie()

        self.id = self.cookie[self.COOKIE_NAME].value
        self.load()

        atexit.register(self.save)

    def session_cookie(self):
        cookie = SimpleCookie()
        if "HTTP_COOKIE" in environ:
            cookie.load(environ["HTTP_COOKIE"])

        if self.COOKIE_NAME not in cookie:
            cookie[self.COOKIE_NAME] = uuid4().hex

        return cookie

    def session_file(self):
        return "%s/%s" % (self.SESSIONS_DIR, self.id)

    def load(self):
        filename = self.session_file()
        if not isfile(filename):
            return {}

        try:
            fo = open(filename, "rb")
            session = load(fo)
            fo.close()

            assert isinstance(session, dict), "bad session file"
            self.update(session)

        except (PickleError, IOError, EOFError):
            # FIXME: Log or something
            return {}

    def save(self):
        if not isdir(self.SESSIONS_DIR):
            try:
                mkdir(self.SESSIONS_DIR)
            except OSError:
                # FIXME: Log or something
                return

        filename = self.session_file()
        try:
            fo = open(filename, "wb")
            dump(self, fo, protocol=-1)
            fo.close()

        except (PickleError, IOError):
            # FIXME: Log or something
            pass
