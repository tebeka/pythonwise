#!/usr/bin/env python
'''Disable/enable connection to Adconion Jabber in Pidgin using dbus'''

import dbus
from os import environ

def is_valid_status(status):
    return 'enable'.startswith(status) or 'disable'.startswith(status)

def get_interface():
    bus = dbus.SessionBus()
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    return dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

def name_of(status):
    return ['disabled', 'enabled'][status]

def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='enable/disable adcoion on pidgin')
    parser.add_argument('status', help='status to set (enable|disable)')
    args = parser.parse_args(argv[1:])

    status = args.status.lower()
    if not is_valid_status(status):
        raise SystemExit('error: bad status - {0}'.format(status))

    purple = get_interface()

    user = '{0}@adconion.com'.format(environ['USER'])
    account = purple.PurpleAccountsFind(user, 'prpl-jabber')
    if not account:
        raise SystemExit('error: no account for {0}'.format(user))

    enabled = 1 if status.startswith('e') else 0

    ui = purple.PurpleCoreGetUi()
    current = purple.PurpleAccountGetEnabled(account, ui)
    if current == enabled:
        print('Nothing to do (already {0})'.format(name_of(current)))
        raise SystemExit

    purple.PurpleAccountSetEnabled(account, ui, enabled)
    print('{0} adconion (was {1})'.format(name_of(enabled), name_of(current)))

if __name__ == '__main__':
    main()
