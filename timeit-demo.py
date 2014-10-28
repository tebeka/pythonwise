#!/usr/bin/env python

from timeit import Timer

def fast_fib(n):
    if n < 2:
        return 1

    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b

    return b

def slow_fib(n):
    if n < 2:
        return 1

    return slow_fib(n - 1) + slow_fib(n - 2)


INDEX = 20
TIMES = 100

fast_timer = Timer("fast_fib(INDEX)", "from __main__ import fast_fib, INDEX")
slow_timer = Timer("slow_fib(INDEX)", "from __main__ import slow_fib, INDEX")

print "slow:", slow_timer.timeit(TIMES) / TIMES
print "fast:", fast_timer.timeit(TIMES) / TIMES
