#!/usr/bin/env python
'''Show last letter frequency in English words'''

from urllib import urlopen
from collections import Counter
from matplotlib import pyplot as plt
import numpy as np


def get_words():
    '''Get list of dictionary words.'''
    # The North American Scrabble Tournament Word List (178,690 words)
    fo = urlopen('http://norvig.com/ngrams/TWL06.txt')
    return (w.strip() for w in fo)


def plot(freq, filename):
    '''Bar chart of last letter frequency.'''
    width = 0.35  # Bar width (also used for xticks positioning)

    idx = np.arange(len(freq))
    xs = sorted(freq)
    ys = [freq[x] for x in xs]

    plt.bar(idx, ys, width=width)
    plt.xticks(idx + width/2., xs)
    plt.title('Last Letter Frequency')
    plt.savefig(filename)


if __name__ == '__main__':
    freq = Counter(w[-1].upper() for w in get_words())
    plot(freq, 'll-freq.png')
