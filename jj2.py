#!/usr/bin/env python
'''Command line for expanding Jinja2 templates.

Template variables can be passed either via the command line (using -vX=Y) or
via a JSON/YAML configuration file (using -i /path/to/vars.json)

Example:

    $ echo 'Hello {{name}}' > template.txt
    $ jj2.py -v name=Bugs template.txt
    Hello Bugs
    $
'''

import jinja2
import json


def load_vars(filename):
    with open(filename) as fo:
        if filename.lower().endswith('.json'):
            return json.load(fo)
        elif filename.lower().endswith('.yaml'):
            import yaml  # Lazy import
            return yaml.load(fo)
        else:
            raise ValueError('unknown file type: {}'.format(filename))


def parse_cmdline_vars(cmdline_vars):
    return dict(var.split('=', 1) for var in cmdline_vars)


def main(argv=None):
    import sys
    from argparse import ArgumentParser, FileType

    argv = argv or sys.argv

    parser = ArgumentParser(description='Expand Jinja2 template')
    parser.add_argument('template', help='template file to expand',
                        type=FileType('r'), nargs='?', default=sys.stdin)
    parser.add_argument('--var', '-v', action='append',
                        help='template variables (in X=Y format)')
    parser.add_argument('--output', '-o', help='output file',
                        type=FileType('w'), nargs='?', default=sys.stdout)
    parser.add_argument('--vars-file', '-i', help='vars files (YAML or JSON)',
                        nargs='?')

    args = parser.parse_args(argv[1:])

    tvars = {}
    if args.vars_file:
        tvars.update(load_vars(args.vars_file))

    tvars.update(parse_cmdline_vars(args.var or []))

    # Fail on undefined
    env = jinja2.Environment(undefined=jinja2.StrictUndefined)
    template = env.from_string(args.template.read())

    args.output.write(template.render(tvars))


if __name__ == '__main__':
    main()
