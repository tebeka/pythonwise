#!/usr/bin/env python
def fast_fib(n):
    if n < 2:
        return 1

    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b

    return b

def benchmark():
    from timeit import Timer

    benchmark.index = 20
    timer = Timer("fast_fib(benchmark.index)",
                  "from __main__ import fast_fib, benchmark")
    num_runs = 100

    print timer.timeit(num_runs) / num_runs

def main(argv=None):
    if argv is None:
        import sys
        argv = sys.argv

    from optparse import OptionParser

    parser = OptionParser("usage: %prog [options] INDEX")
    parser.add_option("--benchmark", help="run benchmark",
                      dest="benchmark", action="store_true", default=0)

    opts, args = parser.parse_args(argv[1:])

    if opts.benchmark:
        benchmark()
        raise SystemExit()

    if len(args) != 1:
        parser.error("wrong number of arguments") # Will exit

    # Do main program stuff here
    try:
        print fast_fib(int(args[0]))
    except ValueError:
        raise SystemExit("error: %s - bad number" % args[0])

if __name__ == "__main__":
    main()
