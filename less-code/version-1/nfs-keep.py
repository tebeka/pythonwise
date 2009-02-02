#!/usr/bin/env python
'''Keep NFS mount "warm"'''

from os import listdir
from time import sleep

if __name__ == "__main__":
    while 1:
        listdir("/path/to/nfs")
        sleep(10 * 60 * 60)
