#!/usr/bin/env python2
"""Export GAE model to dot format."""

# Usage example:
#    ./ndb2dot.py cool.model | dot -Tpng -o model.png
# Install graphviz to get the dot command line utility

from inspect import isclass
from os import environ
import imp
import sys

# Inject GAE SDK path
sys.path.insert(0, environ.get('GAE_PY_SDK', '/opt/google_appengine'))
import dev_appserver  # noqa
dev_appserver.fix_sys_path()
from google.appengine.ext import ndb  # noqa

header = '''\
digraph G {
    graph [rankdir=LR];
    node [shape=none];
'''


def load_module(name):
    """Load module from name"""
    mod = None
    for mod_name in name.split('.'):
        file, pathname, desc = imp.find_module(mod_name, mod and mod.__path__)
        mod = imp.load_module(mod_name, file, pathname, desc)

    return mod


def models(module):
    """Sorted list (by name) of models in module"""
    for attr in dir(module):
        obj = getattr(module, attr)
        if isclass(obj) and issubclass(obj, ndb.Model):
            yield obj


def prop_type(prop):
    """Property type (string)"""
    if isinstance(prop, ndb.StructuredProperty):
        return prop._modelclass.__name__
    name = prop.__class__.__name__
    suffix = 'Property'
    if name.endswith(suffix):
        name = name[:-len(suffix)]
    return name


def model2dot(model):
    """dot represtantation of model"""
    cls = model.__name__
    print('''\
    %s [
        label = <<table>
        <tr><td colspan="2"><b>%s</b></td></tr>''' % (cls, cls))

    links = []

    for name, prop in sorted(model._properties.iteritems()):
        if isinstance(prop, ndb.StructuredProperty):
            port = 'port="%s"' % name
            links.append((name, prop))
        else:
            port = ''
        print('%s<tr><td %s>%s</td><td>%s</td></tr>' % (
              ' ' * 8, port, name, prop_type(prop)))

    print('''\
        </table>>
    ];''')

    for name, prop in links:
        print('    %s:%s -> %s;' % (cls, name, prop_type(prop)))


if __name__ == '__main__':
    from operator import attrgetter
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('module', help='module name (e.g. "cool.model")')
    args = parser.parse_args()

    try:
        mod = load_module(args.module)
    except ImportError as err:
        raise SystemExit('error: cannot load %r - %s' % (args.module, err))

    print(header)

    for model in sorted(models(mod), key=attrgetter('__name__')):
        model2dot(model)

    print('}')
