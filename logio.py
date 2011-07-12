#!/usr/bin/env python

class logio:
    '''Class to emulate file IO for log files'''
    def __init__(self, logfn, strip=False):
        '''logfn
                Log function (such as logging.error ...)
           strip
                Flag to strip data (since logging appends newline)
        '''
        self.logfn = logfn
        self.strip = strip

    def write(self, data):
        if self.strip:
            data = data.rstrip()
        self.logfn(data)

if __name__ == '__main__':
    # Example showing creation of CSV log files
    import csv
    import logging as log

    log.basicConfig(format='%(message)s')

    writer = csv.writer(logio(log.error, True))
    for i in range(10):
        writer.writerow([i, i+1, i+2])
