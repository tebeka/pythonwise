from dataclasses import dataclass


@dataclass
class Location:
    x: int
    y: int


def get_default(locs, name):
    return locs.get(name, Location(0, 0))


def get_none(locs, name):
    loc = locs.get(name)
    if loc is None:
        loc = Location(0, 0)
    return loc
