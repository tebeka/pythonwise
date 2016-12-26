#!/usr/bin/env python
"""Run a flow of BigQuery queries.

We assume the destination table has the same name as the SQL file containing
the query (e.g. "users.sql" will populate the "users" table).

The view functionality requires the "dot" utility (from graphviz).

Scripts are assuming to use "standard" SQL format.
"""

from collections import defaultdict
from glob import iglob
from os import path, SEEK_SET
from subprocess import check_call
from sys import platform
from tempfile import NamedTemporaryFile
import re


def file2table(fname):
    """
    >>> file2table('/path/to/users.sql')
    'users'
    """
    return path.basename(fname)[:-4]


def iter_deps(root):
    """Iterate of table dependencies in scripts in root directory."""
    for sql_file in iglob('{}/*.sql'.format(root)):
        # '/path/to/users.sql' -> 'users'
        dest = file2table(sql_file)
        with open(sql_file) as fp:
            for line in fp:
                for src in re.findall('`([^`]+)`', line):
                    if '.' not in src:
                        msg = 'table without dataset - "{}"'.format(src)
                        raise ValueError(msg)
                    # 'ds1.table2' -> 'table2'
                    src = src[src.rfind('.')+1:]
                    yield src, dest


def view(deps):
    """Generate image of dependency graph and shows it.

    Requires "dot" utility.
    """
    tmp = NamedTemporaryFile()
    tmp.write('''
        digraph G {
            graph[rankdir=LR];
            node[shape=box];
            edge[color=blue];
    '''.encode('utf-8'))
    for src, dest in deps:
        line = '"{}" -> "{}";'.format(src, dest)
        tmp.write(line.encode('utf-8'))
    tmp.write('}\n'.encode('utf-8'))
    tmp.flush()

    tmp.seek(0, SEEK_SET)
    png = '{}.png'.format(tmp.name)
    check_call(['dot', '-Tpng', '-o', png], stdin=tmp)
    cmd = {
        'win32': 'start',
        'darwin': 'open',
    }.get(platform, 'xdg-open')
    check_call([cmd, png])


def run_script(fname, dest, dry_run=False):
    """Run a script using bq utility, send output to dest.

    If dry_run is True, just print commands.
    """
    cmd = [
        'bq', 'query',
        '--destination_table', dest,
        '--replace',
        '--nouse_legacy_sql',
    ]

    if dry_run:
        print(' '.join(cmd) + ' < {}'.format(fname))
        return

    with open(fname) as fp:
        check_call(cmd, stdin=fp)


def dir_type(value):
    """Check that argument is a directory."""
    if not path.isdir(value):
        raise ValueError('{} is not a directory'.format(value))
    return value


# Inspired by
# http://blog.jupo.org/2012/04/06/topological-sorting-acyclic-directed-graphs/
def topological_sort(deps):
    """Return nodes sorted in topological order."""
    graph = defaultdict(list)
    for table, dep in deps:
        graph[table].append(dep)

    while graph:
        cycle = True
        for table, deps in list(graph.items()):
            for dep in deps:
                if dep in graph:
                    break
            else:
                cycle = False
                del graph[table]
                yield table
        if cycle:
            raise ValueError('cycle in graph')


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('root', help='SQL files directory', type=dir_type)
    parser.add_argument(
        '--view', help='view dependency graph (no execution)',
        action='store_true', default=False)
    parser.add_argument(
        '--dry-run', help='print commands (no execution)',
        action='store_true', default=False)
    parser.add_argument(
        '--verbose', '-v', help='be more verbose', action='store_true',
        default=False)
    args = parser.parse_args()

    deps = iter_deps(args.root)
    if args.view:
        view(deps)
        raise SystemExit

    for table in topological_sort(deps):
        fname = '{}/{}.sql'.format(args.root, table)
        if not path.isfile(fname):
            if args.verbose:
                print('skipping {}'.format(fname))
            continue
        run_script(fname, table, args.dry_run)
