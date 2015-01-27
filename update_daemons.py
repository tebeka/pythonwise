#!/usr/bin/env python
'''Bring deamons up/down using supervisord configuration'''

from ConfigParser import ConfigParser
from cStringIO import StringIO
from subprocess import check_call

cfg_file = 'supervisord.conf'

header = '''
[inet_http_server]
port = :9001 ; Listen on all interfaces

[supervisord]

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = \
        supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=http://localhost:9001
'''

prog = 'httpd'


def sect_name(port):
    return 'program:%s-%s' % (prog, port)


def add_sect(cfg, port):
    sect = sect_name(port)
    cfg.add_section(sect)
    cfg.set(sect, 'command', 'python -m SimpleHTTPServer %s' % port)
    cfg.set(sect, 'autorestart', 'true')
    cfg.set(sect, 'redirect_stderr', 'true')  # Log stderr as well


def initial_config(ports):
    cfg = ConfigParser()
    cfg.readfp(StringIO(header))
    for port in ports:
        add_sect(cfg, port)
    return cfg


def load_config(filename):
    cfg = ConfigParser()
    cfg.read(filename)
    return cfg


def save_config(cfg, filename):
    with open(filename, 'w') as out:
        cfg.write(out)


def sect_port(sect):
    '''
        >>> sect_port('program:httpd-8080')
        8080
    '''
    return int(sect.split('-')[-1])


def update_config(cfg, ports):
    prefix = sect_name('')
    current = set(
        sect_port(sect)
        for sect in cfg.sections()
        if sect.startswith(prefix)
    )

    added = set(ports) - set(current)
    for port in added:
        add_sect(cfg, port)

    deleted = set(current) - set(ports)
    for port in deleted:
        cfg.remove_section(sect_name(port))

    return added, deleted


def gen_cmd(action, port):
    return ['supervisorctl', action, '%s-%s' % (prog, port)]


def main():
    from argparse import ArgumentParser
    from os.path import isfile

    parser = ArgumentParser(description='update daemon fleet')
    parser.add_argument('ports', metavar='PORT', type=int, nargs='+',
                        help='port to listen on')
    args = parser.parse_args()

    if not isfile(cfg_file):
        cfg = initial_config(args.ports)
        cmds = [['supervisord']]
    else:
        cfg = load_config(cfg_file)
        added, removed = update_config(cfg, args.ports)
        cmds = [['supervisorctl', 'reread']]
        cmds += [gen_cmd('stop', port) for port in removed]
        cmds += [gen_cmd('remove', port) for port in removed]
        cmds += [gen_cmd('add', port) for port in added]

    save_config(cfg, cfg_file)
    for cmd in cmds:
        check_call(cmd)


if __name__ == '__main__':
    main()
