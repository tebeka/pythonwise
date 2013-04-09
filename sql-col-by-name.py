'''Get columns by name from SQL query'''

import sqlite3
db = sqlite3.connect(":memory:")
db.row_factory = sqlite3.Row

import psycopg2
from psycopg2.extras import DictCursor
db = psycopg2.connect("my-dbn-string")
cur = db.cursor(cursor_factory=DictCursor)

#for row in cur.execute("select * from people"):
#    print row["name"]
