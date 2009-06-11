#!/usr/bin/env python
# A twitter trends/google news mesh

import json
from urllib import urlopen, urlencode
import feedparser
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from os.path import dirname, join, splitext

def trend_news(trend):
    query = {
        "q" : trend,
        "output" : "rss"
    }
    url = "http://news.google.com/news?" + urlencode(query)
    feed = feedparser.parse(url)
    return map(lambda e: {"url" : e.link, "title" : e.title}, feed.entries)

def current_trends():
    url = "http://search.twitter.com/trends.json"
    return json.load(urlopen(url))["trends"]

def news_html(news):
    html = '<li><a href="%(url)s">%(title)s</a></li>'
    chunks = map(lambda s: html % s, news)
    return "\n".join(["<ul>"] + chunks + ["</ul>"])

def trend_html(trend):
    return {
        "trend" : '<li><a class="trend" href="%(url)s">%(name)s</li>' % trend,
        "url" : trend["url"],
        "news" : news_html(trend_news(trend["name"])),
    }

def index_html():
    return open(join(dirname(__file__), "index.html")).read()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.wfile.write(index_html())
        elif self.path.startswith("/get"):
#             html = map(trend_html, current_trends())
#             json.dump(html, self.wfile)
            self.wfile.write(open("t.json").read())
        elif splitext(self.path)[1] in (".js", ".css"):
            self.wfile.write(open(".%s" % self.path).read())
        else:
            self.send_error(404, "Not Found")

if __name__ == "__main__":
    server = HTTPServer(("", 8888), RequestHandler)
    server.serve_forever()

