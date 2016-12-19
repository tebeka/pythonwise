#!/usr/bin/env python
# flake8: noqa

# Fix blog posts to point to github

import requests

from os import path, environ
import json
import re

bid = 27854051
pid = 6308066059358524587
key = environ.get('BLOGGER_API_KEY')

assert key, 'BLOGGER_API_KEY environment variable not set'

api_url = 'https://www.googleapis.com/blogger/v3/blogs/{}/posts'.format(bid)


def get_posts():
    fname = 'posts.json'
    if path.exists(fname):
        with open(fname) as fp:
            return json.load(fp)

    params = {
        'key': key,
        'maxResults': '200',
        'status': 'live',
        'fields': 'items(content,id)',
    }
    resp = requests.get(api_url, params=params)
    posts = resp['items']
    with open(fname, 'w') as out:
        json.dump(posts, out)
    return posts

fixes = [
    # nbviewer
    (
        'http(s)?://nbviewer.(ipython|jupyter).org/urls/bitbucket.org/tebeka/pythonwise/raw/tip/([^" ]+)',
        r'https://nbviewer.jupyter.org/github/tebeka/pythonwise/blob/master/\3',
    ),
    # embed
    (
        '<script src="https://bitbucket.org/tebeka/pythonwise/src/tip/(.+)\?embed=t"></script>',
        r'<script src="http://gist-it.appspot.com/https://github.com/tebeka/pythonwise/blob/master/\1"></script>',
    ),
    # file
    (
        'https://bitbucket.org/tebeka/pythonwise/raw/tip/([^" ]+)',
        r'https://github.com/tebeka/pythonwise/blob/master/\1',
    ),
    # directory
    (
        'https://bitbucket.org/tebeka/pythonwise/src/tip/([^ "]+)/',
        r'https://github.com/tebeka/pythonwise/tree/master/\1',
    ),
]

posts = get_posts()

fixed = []

for post in posts:
    content = post['content']
    for pat, repl in fixes:
        content = re.sub(pat, repl, content)
    changed = post['content'] != content
    post['content'] = content
    if changed:
        fixed.append(post)

for post in fixed:
    print(post['id'])
    url = '%s/%s' % (api_url, post['id'])
    params = {
        'key': key,
    }
    body = {
        'content': post['content'],
    }
    resp = requests.patch(url, json=body, params=params)
    resp.raise_for_status()

# vim: tw=0
