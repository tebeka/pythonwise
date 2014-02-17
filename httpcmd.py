#!/usr/bin/env python
'''HTTP interface to run commands on a machine.

Excepts JSON POST or GET requests with argv, and stdin parameters. Returns a
JSON object with stdout, stderr and returncode attributes.

Run with:

    # with auth
    ./httpcmd.py --user=daffy --password=duck

    # no auth
    ./httpcmd.py

Calling example:

    curl \\
        -H 'Content-Type: application/json' \\
        -d '{"argv": ["ls", "/tmp"]}' \\
        -u daffy:duck \\
        http://localhost:8080
'''

from flask import Flask, request, abort, jsonify

from subprocess import Popen, PIPE
import httplib

app = Flask(__name__)

user, password = None, None


@app.route('/', methods=['GET', 'POST'])
def index():
    if user:
        auth = request.authorization
        ok = auth and (auth.username == user) and (auth.password == password)
        if not ok:
            abort(httplib.UNAUTHORIZED)

    data = request.json
    if not isinstance(data, dict):
        abort(httplib.BAD_REQUEST)

    argv = data.get('argv')
    if argv is None:
        abort(httplib.BAD_REQUEST)
    stdin = data.get('stdin')

    pipe = Popen(argv, stdout=PIPE, stderr=PIPE)
    stdout, stderr = pipe.communicate(stdin)

    return jsonify(
        stdout=stdout,
        stderr=stderr,
        returncode=pipe.returncode,
    )


def main(argv=None):
    global user, password

    import sys
    from argparse import ArgumentParser, RawDescriptionHelpFormatter

    argv = argv or sys.argv

    parser = ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('--port', type=int, help='port', default=8080)
    parser.add_argument('--user', help='auth user')
    parser.add_argument('--password', help='auth password')
    parser.add_argument('--debug', help='run in debug mode', default=False,
                        action='store_true')
    args = parser.parse_args(argv[1:])

    user, password = args.user, args.password
    if bool(user) != bool(password):
        raise SystemExit('error: either both user/password or none')

    app.run(port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
