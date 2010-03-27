#!/usr/bin/env python

from operator import attrgetter
from random import shuffle

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

def sort1(points):
    points.sort(key = lambda p: p.x)

def sort2(points):
    points.sort(key = attrgetter("x"))

if __name__ == "__main__":
    from timeit import Timer

    points1 = [Point(x, 2 * x) for x in range(100)]
    points2 = points1[:]

    num_times = 10000

    t1 = Timer("sort1(points1)", "from __main__ import sort1, points1")
    print t1.timeit(num_times)

    t2 = Timer("sort2(points2)", "from __main__ import sort2, points2")
    print t2.timeit(num_times)
