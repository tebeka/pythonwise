#!/usr/bin/env python
'''Populate with dummy data.'''

from pull import cursor

from random import randint, random
from collections import namedtuple

sql = '''
INSERT INTO points (
    x
  , y
  , z
  , value
) VALUES (
    %s
  , %s
  , %s
  , %s
)'''

Point = namedtuple('Point', ['x', 'y', 'z'])


def rand_coord():
    return randint(0, 1000)


def rand_point():
    return Point(
        rand_coord(),
        rand_coord(),
        rand_coord(),
    )


def gen_points(count):
    coords = set()
    while len(coords) < count:
        coords.add(rand_point())
    return coords



if __name__ == '__main__':
    pre_cur = cursor('pre')
    post_cur = cursor('post')

    points = gen_points(10000)
    for point in points:
        pre_value = random() * 1000
        post_value = pre_value

        # In 1% probability, generate different value
        if random() <= 0.01:
            # Up to 10% difference
            diff = (random() * 0.1) * pre_value
            if random() > 0.5:
                post_value += diff
            else:
                post_value -= diff

        pre_cur.execute(sql, (point.x, point.y, point.z, pre_value))
        post_cur.execute(sql, (point.x, point.y, point.z, post_value))

    pre_cur.connection.commit()
    post_cur.connection.commit()
