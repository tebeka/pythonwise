'''Using pyodbc with Netezza example'''
import pyodbc

user = '"daffy.duck"'  # Need quotes
password = 'ThisMeansWar'
server = 'planet.looney'
database = 'bugs'

dsn = 'DRIVER=\{NetezzaSQL\};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (server, database, user, password)
conn = pyodbc.connect(dsn)

with conn.cursor() as cur:
    cur.execute("select * from BUGS..MONEY")
    for row in cur:
        print(row)
