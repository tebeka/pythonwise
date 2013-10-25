# Simple Python based configuration system

# Usage:
# If this file is in PYTHONPATH, then 'import config'
# Otherwise, something like the following should work (Python 2x)
#
#    from os.path import dirname
#    import sys
#
#    def load_config(path):
#        class _cfg: pass
#        cfg = _cfg()
#
#        parent = dirname(path)
#        sys.path.insert(0, parent)
#        try:
#            execfile(path, {}, cfg.__dict__)
#            return cfg
#        finally:
#            sys.path.pop(0)

# Overrideable configuration, keep it flat
web_host = 'localhost'
web_port = 8080

# Overriding is easy, just add config_local.py and write the values you want to
# change. In this example we have only the line 'web_port = 8000' in
# config_local.py
try:
    from config_local import *  # NOQA
except ImportError:  # Catch only ImportError here
    pass

# Here's it after overriding, we can construct more Pythonic objects here

web = {
    'host': web_host,
    'port': web_port
}

# Print configuration, for use in shell scripts
# (e.g. webhost=$(python config.py web_host))

if __name__ == '__main__':
    # Start with _ so they won't show up as configuration key
    from argparse import ArgumentParser as _AP
    _parser = _AP('configuration')
    _parser.add_argument('key', nargs='?', help='configuration key')

    _args = _parser.parse_args()

    env = dict(
        (key, value) for key, value in locals().items() if key[0] != '_')

    if _args.key:
        if _args.key not in env:
            raise SystemExit('error: {} not found'.format(_args.key))
        print(env[_args.key])
    else:
        for key, value in sorted(env.iteritems()):
            print('{}={}'.format(key, value))
