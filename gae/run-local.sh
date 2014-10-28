#!/bin/bash
# Run development server on given port, we listen on 0.0.0.0 so we can access it
# from outside of localhost

port=${1-8080}

/opt/python2.5/bin/python \
    /opt/google_appengine/dev_appserver.py -p $port -a 0.0.0.0 .
