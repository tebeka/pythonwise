#!/usr/bin/env python
'''Annotate mercurial branches with issue description from JIRA.

You'll need ~/.jira-login.json with your jira credentials in the following
format::

    {
        "user" : "your-jira-user-name",
        "password" : "your-jira-password"
    }
'''

from subprocess import check_output
from xmlrpclib import ServerProxy
from os.path import expanduser
import re
import json

JIRA_URL = 'http://localhost/jira/rpc/xmlrpc'

def jira_credentials():
    '''User JIRA credentials.'''
    with open(expanduser('~/.jira-login.json')) as fo:
        data = json.load(fo)
        return data['user'], data['password']

def jira_connect(user, password):
    '''Connect to JIRA, return proxy object and token.'''
    jira = ServerProxy().jira1
    token = jira.login(user, password)
    return jira, token

def branches(project):
    '''Leave only branches that are in the format PROJECT-XXXX.'''
    return re.findall('{0}-\\d+'.format(project),
                       check_output(['hg', 'branches']))

def branch_parent(branch):
    '''Return parent branch of current branches.'''
    # Taken from http://bit.ly/tmRYNw
    # FIXME: Sometimes this doesn't show the right branch
    parent = check_output(['hg', 'log', '--template', '{branches}',
                           '-r', 'parents(min(branch("{0}")))'.format(branch)])
    return parent.strip()

def issue_description(key, jira, token):
    '''Get issue description from JIRA.'''
    return jira.getIssue(token, key)['summary']

def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(
        description='Annotate branches with JIRA issue description')
    parser.add_argument('-p', '--project', default='PROJECT',
                        help='project name (default is PROJECT)')
    parser.add_argument('-j', '--jira-url', default=JIRA_URL,
                        help='JIRA URL ({0})'.format(JIRA_URL))
    args = parser.parse_args(argv[1:])

    user, password = jira_credentials()
    jira, token = jira_connect(user, password)

    for branch in branches(args.project):
        desc = issue_description(branch, jira, token)
        parent = branch_parent(branch)
        if parent != 'default':
            desc = '{0} [{1}]'.format(desc, parent)
        print("{0}: {1}".format(branch, desc))

if __name__ == '__main__':
    main()

