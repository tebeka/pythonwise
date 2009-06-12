#!/usr/bin/env python
# A twitter trends/google news mesh

from urllib import urlopen, urlencode
import feedparser
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from os.path import dirname, join, splitext
import json
from threading import Thread
from time import sleep

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
   thtml = '<a class="trend" href="%(url)s">%(name)s' % trend
   nhtml = news_html(trend_news(trend["name"]))
   return '<tr><td class="trend">%s</td><td>%s</td><tr>' % (thtml, nhtml)

def table_html(trends):
    return ("<table>" + 
            "<tr><th>Trend</th><th>Related News</th></tr>" +
            "".join(map(trend_html, trends)) +
            "</table>"
           )

_TRENDS_HTML = ""
def loader_thread():
    global _TRENDS_HTML

    while 1:
        html = table_html(current_trends())
        html = html.encode("ascii", "ignore") # Pure ACII

        _TRENDS_HTML = html
        sleep(60)

def run_loader_thread():
    t = Thread(target=loader_thread)
    t.daemon = 1
    t.start()

def trends_html():
    while not _TRENDS_HTML:
        sleep(0.1)

    return _TRENDS_HTML

def index_html():
    return open(join(dirname(__file__), "index.html")).read()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.wfile.write(index_html())
        elif self.path.startswith("/trends"):
            self.wfile.write(trends_html())
        elif splitext(self.path)[1] in (".js", ".css"):
            self.wfile.write(open(".%s" % self.path).read())
        else:
            self.send_error(404, "Not Found")

if __name__ == "__main__":
    run_loader_thread()
    server = HTTPServer(("", 8888), RequestHandler)
    server.serve_forever()

