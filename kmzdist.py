#!/usr/bin/env python
# encoding: utf-8
'''Calculate distance of path in .kmz file in Km'''

from collections import namedtuple
from math import sqrt, sin, cos, atan2, radians
from zipfile import ZipFile, BadZipfile
import xml.etree.ElementTree as et

namespaces = {'gx': 'http://www.google.com/kml/ext/2.2'}
Coord = namedtuple('Coord', ['lat', 'lng'])
R = 6371  # Earth radium in km


def elem2coord(elem):
    # '35.014666 32.519769 144.1999969482422' -> (35.014666, 32.519769)
    lat, lng, _ = [float(v) for v in elem.text.split()]
    return Coord(lat, lng)


def sin2(x):
    '''sin²(x/2)'''
    v = sin(x/2.)
    return v * v


def dist(coord1, coord2):
    '''Distance between two coordinates

        This uses the ‘haversine’ formula to calculate the great-circle
        distance between two points – that is, the shortest distance over the
        earth’s surface – giving an ‘as-the-crow-flies’ distance between the
        points (ignoring any hills they fly over, of course!).

        Haversine formula:
            a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
            c = 2 ⋅ atan2( √a, √(1−a) )
            d = R ⋅ c
        where	φ is latitude, λ is longitude, R is earth’s radius (mean radius
        = 6,371km);

      via http://www.movable-type.co.uk/scripts/latlong.html
    '''
    lat1, lng1 = radians(coord1.lat), radians(coord1.lng)
    lat2, lng2 = radians(coord2.lat), radians(coord2.lng)

    a = sin2(abs(lat2 - lat1)) + cos(lat1) * cos(lat2) * sin2(abs(lng2 - lng1))
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


def kmz_dist(file):
    '''Calculate distance of all points in .kmz file in Km

    file can be either a file name or an open file object.
    '''
    zfo = ZipFile(file)
    fo = zfo.open(zfo.filelist[0].filename)

    root = et.parse(fo).getroot()
    elems = root.iterfind('.//gx:coord', namespaces=namespaces)
    coords = [elem2coord(elem) for elem in elems]

    # Shift the coords list and then zip with itself, we'll get a list of
    # tuples like [(coord1, coord2), (coord2, coord3) ...]
    return sum(dist(c1, c2) for c1, c2 in zip(coords, coords[1:]))


if __name__ == '__main__':
    from argparse import ArgumentParser
    from sys import stdin

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('kmz', help='kmz file name', default='-', nargs='?')
    args = parser.parse_args()

    file = stdin if args.kmz == '-' else args.kmz
    try:
        print('{:.3f}km'.format(kmz_dist(file)))
    except (IOError, BadZipfile) as err:
        raise SystemExit('error: {}'.format(err))
