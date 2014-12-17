#!/usr/bin/env python

# Example CGI implementation

# Database schema:
# CREATE TABLE clicks (
#   url TEXT,
#   value TEXT,
# );

from cgi import FieldStorage
import sqlite3



form = FieldStorage()

url = form.getvalue("url", "").strip()
value = form.getvalue("value", "").strip()

if not (url and value):
    raise SystemExit("error: missing parameter")

db = sqlite3.connect("clicks.db")
cur = db.cursor()
cur.execute("INSERT INTO clicks values (?, ?)", (url, value))
db.commit()
