#!/usr/bin/env python
'''Server to show computer load'''

import re
from os import popen
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from socket import gethostname

def load():
    '''Very fancy computer load :)'''
    output = popen("uptime").read()
    match = re.search("load average(s)?:\\s+(\\d+\\.\\d+)", output)
    return float(match.groups()[1]) * 100

HTML = '''
<html>
    <head>
        <script src="jquery.js"></script>
        <script src="jquery.flot.js"></script>
        <title>%s load</title>
    </head>
    <body>
        <center>
            <h1>%s load</h1>
            <div id="chart" style="width:600px;height:400px;">
            Loading ...
            </div>
        </center>
    </body>
    <script>
    var samples = [];
    var options = {
        yaxis: {
            min: 0,
            max: 100
        },
        xaxis: {
            ticks: []
        }
    };

    function get_data() {
        $.getJSON("/data", function(data) {
            samples.push(data);
            if (samples.length > 120) {
                samples.shift();
            }

            var xy = [];
            for (var i = 0; i < samples.length; ++i) {
                xy.push([i, samples[i]]);
            }
            $.plot($('#chart'), [xy], options);
        });
    }

    $(document).ready(function() {
        setInterval(get_data, 1000);
    });
    </script>
</html>
''' % (gethostname(), gethostname())

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.wfile.write(HTML)
        elif self.path.endswith(".js"):
            self.wfile.write(open(".%s" % self.path).read())
        else:
            self.wfile.write("%.2f" % load())

if __name__ == "__main__":
    server = HTTPServer(("", 8888), RequestHandler)
    server.serve_forever()
