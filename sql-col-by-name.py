'''Get columns by name from SQL query'''

import sqlite3
db = sqlite3.connect(":memory:")
db.row_factory = sqlite3.Row

from psycopy2.extras import DictCursor
import psycopy2
db = psycopy2.connect("my-dbn-string")
cur = db.cursor(row_factory=DictCursor)

#for row in cur.execute("select * from people"):
#    print row["name"]
