'''defaultdict demo'''

from collections import defaultdict

def histogram(text):
    histogram = defaultdict(int) # int() -> 0

    for word in text.split():
        histogram[word] += 1

    return histogram

def location_histogram(text):
    histogram = defaultdict(list) # list() -> []

    for location, word in enumerate(text.split()):
        histogram[word].append(location)

    return histogram
