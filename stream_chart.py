#!/usr/bin/env python
'''Show streaming graph of stock.'''


from flask import Flask, jsonify

from collections import deque
from threading import Thread
from time import time, sleep
from urllib import urlopen, urlencode
import csv

html = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Streaming Stocks</title>
    <style>
      #chart {
        min-height: 300px;
      }
    </style>
    <link
      rel="stylesheet"
      href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
  </head>
  <body>
    <div class="container">
    <h4>%(stock)s</h4>
    <div id="chart"></div>
  </body>
  <script
    src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js">
  </script>
  <script
    src="//cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.min.js">
  </script>
  <script
    src="//cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.time.min.js">
  </script>

  <script>
  var chart;

  function get_data() {
    $.ajax({
        url: '/data',
        type: 'GET',
        dataType: 'json',
        success: on_data
    });
  }

  function on_data(data) {
    chart.setData([{data: data.values}]);
    chart.setupGrid();
    chart.draw();

    setTimeout(get_data, 1000);
  }

  $(function() {
    chart = $.plot("#chart", [ ], {xaxis: {mode: "time"}});
    get_data();
  });

    </script>
</html>
'''

app = Flask(__name__)
stock = None
# In memory RRDB
values = deque(maxlen=1000)


def gen_url(stock):
    url = 'http://download.finance.yahoo.com/d/quotes.csv'
    query = {
        's': stock,
        'f': 'nsl1op',
        'e': '.csv',
    }
    return '%s?%s' % (url, urlencode(query))


def poll_data(stock):
    url = gen_url(stock)
    while True:
        fo = urlopen(url)
        for row in csv.reader(fo):
            # "Google Inc.","GOOG",547.04,543.00,540.77
            price = float(row[2])
            break
        values.append((time(), price))
        sleep(3)


@app.route('/')
def home():
    return html % {'stock': stock}


@app.route('/data')
def data():
    # * 1000 to convert to javascript time
    return jsonify(values=[(int(time)*1000, val) for time, val in values])


def main(argv=None):
    global stock

    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='')
    parser.add_argument('stock', help='stock to monitor')
    args = parser.parse_args(argv[1:])

    thr = Thread(target=poll_data, args=(args.stock,))
    thr.daemon = True
    thr.start()

    stock = args.stock  # For html template
    # debug will reload server on code changes
    # 0.0.0.0 means listen on all interfaces
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
