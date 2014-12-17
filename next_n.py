#!/usr/bin/env python

from itertools import ifilter, islice

def next_n(items, pred, count):
 return islice(ifilter(pred, items), count)

if __name__ == "__main__":
 from gmpy import is_prime
 from itertools import count
 for prime in next_n(count(1), is_prime, 10):
     print prime
