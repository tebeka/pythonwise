#!/usr/bin/env python

from itertools import starmap
from random import random, randint, choice
from sys import stdout

MUTATE_PROBABILITY = 0.1

def mutate_gene(n, range):
    if random() > MUTATE_PROBABILITY:
        return n

    while 1:
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
    return map(choice, zip(chromosome1, chromosome2))

def make_chromosome(ranges):
    return tuple(starmap(randint, ranges))

def breed(population, size, ranges):
    new = population[:]
    while len(new) < size:
        new.append(crossover(choice(population), choice(population)))
        new.append(mutate(choice(population), ranges))

    return new[:size]

def evaluate(func, chromosome, data, cache):
    if chromosome not in cache:
        cache[chromosome] = func(chromosome, data)

    return cache[chromosome]

def update_score_cache(population, func, data, cache):
    for chromosome in population:
        if chromosome in cache:
            continue
        cache[chromosome] = func(chromosome, data)

def find_best(popsize, nruns, ranges, func, data):
    score_cache = {}
    best_score = -1
    best_chromosome = None
    population = [make_chromosome(ranges) for i in range(popsize)]
    for generation in xrange(nruns):
        update_score_cache(population, func, data, score_cache)
        population.sort(key=score_cache.get, reverse=1)
        base = population[:popsize/4]
        population = breed(base, popsize, ranges)

    return best_chromosome, best_score

