#!/usr/bin/env python
'''Pull data from database to .h5 storage.'''

# Assuming our points tables have the following schema
# CREATE TABLE points (
#     x INTEGER
#   , y INTEGER
#   , z INTEGER
#   , value FLOAT
# );
# We have two database points_pre and points_post

import psycopg2
from psycopg2.extras import DictCursor
from pandas import DataFrame, HDFStore
from threading import Thread


def cursor(step):
    '''Return a DictCursor connected to step=pre/post database.'''
    conn = psycopg2.connect(database='points_{}'.format(step))
    return conn.cursor(cursor_factory=DictCursor)


if __name__ == '__main__':
    pre_cursor = cursor('pre')
    post_cursor = cursor('post')

    sql = 'SELECT x, y, z, value FROM points'''

    # Get data in two threads to speed things up
    pre_t = Thread(target=pre_cursor.execute, args=(sql,))
    pre_t.start()
    post_t = Thread(target=post_cursor.execute, args=(sql,))
    post_t.start()
    pre_t.join()
    post_t.join()


    # Create data frames
    pre = DataFrame.from_records([dict(row) for row in pre_cursor])
    post = DataFrame.from_records([dict(row) for row in post_cursor])

    # Store data frame in HDF5 data store
    store_file = 'points.h5'
    store = HDFStore(store_file)
    store['pre'] = pre
    store['post'] = post
    store.flush()

    print('Data stored at {}'.format(store_file))
