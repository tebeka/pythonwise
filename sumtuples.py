#!/usr/bin/env python
'''Summarize tuples by key using a sqlite3'''

import sqlite3

def sumtuples(data, key_index):
    # In memory database
    cur = sqlite3.connect(':memory:').cursor()
    cols = ['i{0}'.format(i) for i, _ in enumerate(data[0])]

    # Create table
    schema = 'CREATE TABLE items ({0})'.format(','.join(cols))
    cur.execute(schema)
    cur.connection.commit()

    # Insert data
    sql = 'INSERT INTO items VALUES ({0})'.format(','.join('?' for _ in cols))
    cur.executemany(sql, data)
    cur.connection.commit()

    # SUM and GROUP BY
    key = cols[key_index]
    summed = ','.join(['SUM({0})'.format(col) for col in cols if col != key])
    sql = 'SELECT {0}, {1} FROM items GROUP BY {0}'.format(key, summed)

    cur.execute(sql)
    # Cursor object is iterable, return it
    return cur

if __name__ == '__main__':
    # Small test case
    data = [
        ('a', 1, 2),
        ('b', 2, 3),
        ('a', 1, 2),
        ('b', 2, 3)
    ]

    print(list(sumtuples(data, 0)))
