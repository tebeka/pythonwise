#!/bin/bash
# Push new version to AppEngine and tag in mercurial

set -e

/opt/python2.5/bin/python /opt/google_appengine/appcfg.py update .
hg tag -f appengine
