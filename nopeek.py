#!/usr/bin/env python
'''Avoiding the need for "peek" with itertools.chain'''

from itertools import chain

def is_first_data(line):
    return line.startswith("Name:")

def skip_header(data):
    data = iter(data)
    for line in data:
        if is_first_data(line):
            return chain([line], data)

    # FIXME: We might want to raise something here
    return []


if __name__ == "__main__":
    data = [
        "this is the header",
        "it might change every time",
        "and you'll never find a good regexp for it",
        "The first line of data is easy to know",
        "Name: Duffy",
        "Type: Duck",
        "Anger: 10",
        "",
        "Name: Bugs",
        "Type: Bunny",
        "Anger: 0",
    ]

    data = skip_header(data)
    for line in data:
        print line
