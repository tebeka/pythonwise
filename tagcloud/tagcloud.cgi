#!/usr/bin/env python

import cgitb; cgitb.enable()

from mako.template import Template

from operator import itemgetter
from random import random
from itertools import starmap

MAX_FONT_SIZE = 3
MIN_FONT_SIZE = 0.5

# Arbirary list of tags
TAGS = '''
.net  2008  3d  advertising  ajax  animation  api  apple  architecture  art
article  articles  audio  blog  blogging  blogs  book  books  business  china
code  collaboration  community  computer  cool  css  culture  database  design
development  diy  download  economics  education  environment  fashion  fic
finance  firefox  flash  flex  food  free  freeware  fun  funny  gallery  game
games  google  graphics  green  hardware  health  history  home  howto  html
humor  illustration  images  inspiration  interesting  internet  iphone  java
javascript  jobs  jquery  language  learning  library  lifehacks  linux  mac
maps  marketing  math  media  microsoft  mobile  money  movies  mp3  music  news
online  opensource  osx  photo  photography  photos  photoshop  php  plugin
politics  portfolio  productivity  programming  python  rails  recipe  recipes
reference  research  resources  ruby  science  search  security  seo  shopping
social  socialmedia  socialnetworking  software  tech  technology  tips  tools
toread  travel  tutorial  tutorials  tv  twitter  typography  ubuntu  video
visualization  web  web2.0  webdesign  webdev  wiki  windows  wordpress  work
writing  youtube
'''


def gen_tags():
    '''Generate dummy tag count'''
    return map(lambda tag: (tag, int(random() * 1000)), TAGS.split())

def fontize(tags):
    # Make it float to get real division
    max_value = float(max(map(itemgetter(1), tags)))

    def font(value):
        size = max(MIN_FONT_SIZE, (value / max_value) * MAX_FONT_SIZE)
        return "%0.1fem" % size

    return starmap(lambda tag, count: (tag, font(count)), tags)

def main(argv=None):
    if argv is None:
        import sys
        argv = sys.argv

    from optparse import OptionParser

    parser = OptionParser("usage: %prog")

    opts, args = parser.parse_args(argv[1:])
    if len(args) != 0:
        parser.error("wrong number of arguments") # Will exit

    tags = gen_tags()
    tags = fontize(tags)

    page = Template(filename="tagcloud.mako")

    print "Content-Type: text/html\n"
    print page.render(tags=tags)

if __name__ == "__main__":
    main()
