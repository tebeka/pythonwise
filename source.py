from subprocess import Popen, PIPE
from os import environ

def source(script, update=1):
    pipe = Popen(". %s; env" % script, stdout=PIPE, shell=True)
    data = pipe.communicate()[0]

    env = dict((line.split("=", 1) for line in data.splitlines()))
    if update:
        environ.upadate(env)

    return env
