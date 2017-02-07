from os import path
from glob import iglob
import re


class SQLDir(dict):
    """Fill attribute values from SQL files in a directory"""
    def __init__(self, root):
        self._root = root

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)

    def __missing__(self, key):
        try:
            with open(path.join(self._root, key + '.sql')) as fp:
                val = self[key] = fp.read()
                return val
        except OSError:
            raise KeyError(key)

    def __dir__(self):
        files = iglob(path.join(self._root, '*.sql'))
        bases = (path.basename(file) for file in files)
        return sorted(re.sub('.sql$', '', base) for base in bases)


def example_usage():
    import sqlite3
    sqld = SQLDir('/tmp/sql')

    conn = sqlite3.connect(':memory:')
    if conn.execute(sqld.table_exists).fetchone() is None:
        conn.executescript(sqld.schema)
        conn.commit()
    # ...
