#!/usr/bin/env python2
'''Serving dynamic images with matplotlib (using flask).'''

# No windows should pop up in a web server
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from cStringIO import StringIO

from flask import Flask
app = Flask(__name__)

# HTML template, we embed base64 encoded image data in the <img> HTML element
html = '''
<html>
    <body>
        <img src="data:image/png;base64,{}" />
    </body>
</html>
'''

@app.route("/")
def index():

    # Plot sin and cos between -10 and 10 (1000 points)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = np.linspace(-10, 10, 1000)
    ax.plot(xs, np.sin(xs), label='sin(x)')
    ax.plot(xs, np.cos(xs), label='cos(x)')
    ax.legend()

    # Encode image to png in base64
    io = StringIO()
    fig.savefig(io, format='png')
    data = io.getvalue().encode('base64')

    return html.format(data)


if __name__ == '__main__':
    app.run()
