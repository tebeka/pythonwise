#!/usr/bin/env python

import cgitb; cgitb.enable()
from cgi import FieldStorage

INDEX = '''
<html>
    <head>
        <title>Lighty Dynamic Static Thingie</title>
    </head>
    <body>
        <h1>Get A Chart</h1>
        <form>
            Chart Name: <input name="name" /> <br />
            <input type="submit" value="Click Me" />
        </form>
    </body>
</html>
'''

def main():
    form = FieldStorage()

    name = form.getvalue("name", "").strip()
    if not name:
        print "Content-type: text/html\n"
        print INDEX
        raise SystemExit

    # Redirect to chart
    print "Location: /charts/%s.png\n" % name

if __name__ == "__main__":
    main()
