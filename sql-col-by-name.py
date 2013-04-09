'''Get columns by name from SQL query'''

# sqlite3
import sqlite3
db = sqlite3.connect(':memory:')
db.row_factory = sqlite3.Row

# psycopg2
import psycopg2
from psycopg2.extras import DictCursor
db = psycopg2.connect('my-dbn-string')
cur = db.cursor(cursor_factory=DictCursor)

# Then
cur.execute('select * from people')
for row in cur:
    print(row['name'])
