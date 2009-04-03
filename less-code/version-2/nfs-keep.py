#!/usr/bin/env python
'''Keep NFS mount "warm", called from crontab'''

from os import listdir

if __name__ == "__main__":
    listdir("/path/to/nfs")
