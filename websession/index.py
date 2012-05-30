#!/usr/bin/env python

from websession import WebSession

def main():

    session = WebSession()

    key = 'key'
    old = session.get(key, 0)
    new = old + 1
    session[key] = new

    print(session.cookie)
    html = '''Content-Type: text/html

    <html><body>
    <pre>
    session id: {}
    old: {}
    new: {}
    </pre>
    </body></html>'''.format(key, old, new)
    print(html)

    session.save()

if __name__ == '__main__':
    main()
