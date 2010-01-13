#!/usr/bin/env python

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import urlparse
from urllib2 import urlopen
from operator import itemgetter
from rfc822 import parsedate_tz
from time import strftime
import re
from functools import partial

try:
    import json
except ImportError:
    import simplejson as json

HTML = '''
<html>
    <head>
        <title>Twiver - Refreshing Twitter Search</title>
        <style>
            h2 {
                font-variant: small-caps;
            }
            table#results {
                border: 1px solid black;
                width: 100%;
            }
            table#results tr:hover {
                background: silver;
            }
            span#updated {
                font-family: Monospace;
            }
        </style>
    </head>
    <body>
        <h2>Twiver - Refreshing Twitter Search</h2>
        Query: <input id="query" size="60" /> <button id="run">Go</button>
        <table id="results">
        </table>
        <span id="updated"></span>
        <hr />
        By <a href="mailto:miki@mikitebeka.com">Miki</a>
    </body>
    <script src="jquery.js"></script>
    <script>
        var running = 0;

        function handle_result(data) {
            if (!running) {
                return;
            }

            var table = $('#results');
            table.empty();
            $.each(data, function (i, text) {
                var tr = $('<tr><td>' + text + '</td></tr>');
                table.append(tr);
            });
            $('#updated').html('Updated: ' + new Date());

            setTimeout(update, 1000);
        }

        function update() {
            var query = $.trim($('#query').val());
            $.getJSON('/search', {q: query}, handle_result);
        }

        function run() {
            var button = $('#run');
            if (button.text() == "Go") {
                var query = $.trim($('#query').val());
                /* FIXME: The best way will be to disable the button until there
                  is text
                */
                if (query.length == 0) {
                    alert("Please enter *something*");
                    return;
                }
                button.text("Stop");
                running = 1;
                update();
            }
            else {
                running = 0;
                button.text("Go");
            }
        }

        function on_ready()
        {
            $('#run').click(run);
        }
        $(document).ready(on_ready);
    </script>
</html>
'''

def format_time(time):
    # Wed, 11 Feb 2009 00:10:36 +0000
    time = parsedate_tz(time)
    return strftime("%m/%d/%Y %H:%M", time[:9])

# 'http://mikitebeka.com' -> 
# '<a href="http://mikitebeka.com">http://mikitebeka.com</a>'
inject_links = partial(
    re.compile("(http://[^ ]+)").sub, 
    "<a target=\"_new\" href=\"\\1\">\\1</a>")

def format_result(result):
    time = format_time(result["created_at"])
    text = inject_links(result["text"])
    return "[%s] %s" % (time, text)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.wfile.write(HTML)
        elif self.path.startswith("/search"):
            self.updates()
        elif self.path.endswith(".js"):
            self.wfile.write(open(".%s" % self.path).read())
        else:
            self.send_error(404, "Not Found")

    def updates(self):
        o = urlparse(self.path)
        url = "http://search.twitter.com/search.json?" + o.query
        data = urlopen(url).read()
        obj = json.loads(data)
        results = map(format_result, obj["results"])
        self.wfile.write(json.dumps(results))

if __name__ == "__main__":
    server = HTTPServer(("", 8888), RequestHandler)
    server.serve_forever()

