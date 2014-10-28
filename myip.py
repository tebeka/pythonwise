#!/usr/bin/env python
'''Find local machine IP (cross platform)'''

from subprocess import Popen, PIPE
from sys import platform
import re

COMMANDS = {
    "darwin" : "/sbin/ifconfig",
    "linux" : "/sbin/ifconfig",
    "linux2" : "/sbin/ifconfig",
    "win32" : "ipconfig",
}

def my_ip():
    command = COMMANDS.get(platform, "")
    assert command, "don't know how to get IP for current platform"

    pipe = Popen([command], stdout=PIPE)
    pipe.wait()
    output = pipe.stdout.read()

    for ip in re.findall("(\d+\.\d+\.\d+\.\d+)", output):
        if ip.startswith("127.0.0"):
            continue
        return ip

if __name__ == "__main__":
    print my_ip()
