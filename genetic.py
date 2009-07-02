#!/usr/bin/env python
'''Playing with genetic algorithms, see 
http://en.wikipedia.org/wiki/Genetic_programming.

The main idea that the "chromosome" represents variables in our algorithm and we
have a fitness function to check how good is it. For each generation we keep the
best and then mutate and crossover some of them.

Since the best chromosomes move from generation to generation, we cache the
fitness function results.

I'm pretty sure I got the basis for this from somewhere on the net, just don't
remeber where :)
'''

from itertools import starmap
from random import random, randint, choice
from sys import stdout

MUTATE_PROBABILITY = 0.1

def mutate_gene(n, range):
    if random() > MUTATE_PROBABILITY:
        return n

    while 1:
        # Make sure we mutated something
        new = randint(range[0], range[1])
        if new != n:
            return new

def mutate(chromosome, ranges):
    def mutate(gene, range):
        return mutate_gene(gene, range)

    while 1:
        new = tuple(starmap(mutate, zip(chromosome, ranges)))
        if new != chromosome:
            return new

def crossover(chromosome1, chromosome2):
    return tuple(map(choice, zip(chromosome1, chromosome2)))

def make_chromosome(ranges):
    return tuple(starmap(randint, ranges))

def breed(population, size, ranges):
    new = population[:]
    while len(new) < size:
        new.append(crossover(choice(population), choice(population)))
        new.append(mutate(choice(population), ranges))

    return new[:size]

def evaluate(fitness, chromosome, data, cache):
    if chromosome not in cache:
        cache[chromosome] = fitness(chromosome, data)

    return cache[chromosome]

def update_score_cache(population, fitness, data, cache):
    for chromosome in population:
        if chromosome in cache:
            continue
        cache[chromosome] = fitness(chromosome, data)

def find_solution(fitness, data, ranges, popsize, nruns, verbose=0):
    score_cache = {}
    population = [make_chromosome(ranges) for i in range(popsize)]
    for generation in xrange(nruns):
        update_score_cache(population, fitness, data, score_cache)
        population.sort(key=score_cache.get, reverse=1)
        if verbose:
            best = population[0]
            err = score_cache[best]
            print "%s: a=%s, b=%s, err=%s" % (generation, best[0], best[1], err)

        base = population[:popsize/4]
        population = breed(base, popsize, ranges)

    population.sort(key=score_cache.get, reverse=1)
    return population[0], score_cache[population[0]]

def test(show_graph=1):
    '''Try to find a linear equation a*x + b that is closest to log(x)'''
    from math import log
    xs = range(100)
    data = map(lambda i: log(i+1) * 100, xs)
    def fitness(chromosome, data):
        '''Calculate average error'''
        a, b = chromosome
        def f(x):
            return a * x + b
        values = map(f, xs)
        diffs = map(lambda i: abs(values[i] - data[i]), xs)

        # We want minimal error so return 1/error
        return 1 / (sum(diffs) / len(diffs))

    # Show a nice plot
    (a, b), err = find_solution(fitness, data, ((0, 100), (0, 100)), 10, 100, 1)
    print "best: a=%s, b=%s (error=%s)" % (a, b, err)

    data2 = map(lambda x: a * x + b, range(100))
    if not show_graph:
        return

    import pylab
    l1, l2 = pylab.plot(xs, data, xs, data2)
    pylab.legend((l1, l2), ("log(x+1)", "%s * x + %s" % (a, b)))
    pylab.show()

if __name__ == "__main__":
    test()
