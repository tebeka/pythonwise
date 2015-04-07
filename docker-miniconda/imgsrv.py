#!/usr/bin/env python

from cStringIO import StringIO

from PIL import Image
from flask import Flask, request, make_response
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.transform import resize as _resize
from skimage.util import img_as_ubyte
import numpy as np


app = Flask(__name__)


def data2array(data):
    io = StringIO(data)
    im = Image.open(io)
    return np.array(im)


def as_gray(img):
    return img if len(img.shape) == 2 else rgb2gray(img)


def to_bytes(img, format='png'):
    im = Image.fromarray(img_as_ubyte(img))
    io = StringIO()
    im.save(io, format)
    return io.getvalue()


def img_resonse(img):
    data = to_bytes(img)
    resp = make_response(data)
    resp.headers['Content-Type'] = 'image/png'
    return resp


@app.route('/edge', methods=['POST'])
def edge():
    img = as_gray(data2array(request.data))
    edged = sobel(img)
    return img_resonse(edged)


@app.route('/resize', methods=['POST'])
def resize():
    img = data2array(request.data)
    size = request.args.get('size', '50%')
    # size can be either "30%" or "200x300"
    if size.endswith('%'):
        def conv(val):
            return int(val * float(size[:-1])/100.0)
        width, height = [conv(v) for v in img.shape[:2]]
    else:
        width, height = [int(v) for v in size.split('x')]

    resized = _resize(img, (width, height))
    return img_resonse(resized)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description='image server')
    port = 8080
    parser.add_argument(
        '--port', '-p', type=int, default=port,
        help='port to listen on (%s)' % port)
    parser.add_argument(
        '--debug', '-d', help='debug mode', action='store_true', default=False)
    args = parser.parse_args()

    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=args.port,
        debug=args.debug,
    )
