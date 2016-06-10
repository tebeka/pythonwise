"""Initianlize GAE Python environment so you can work with it from the REPL"""

from os import environ
import sys

sys.path.insert(0, environ.get('GAE_PY_SDK', '/opt/google_appengine'))

import dev_appserver  # noqa
dev_appserver.fix_sys_path()

from google.appengine.ext import testbed  # noqa

tb = testbed.Testbed()
tb.activate()
tb.init_all_stubs()
