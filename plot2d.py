#!/usr/bin/env python
'''Quick and dirty way to show your data.'''

import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.decomposition import PCA

def plot2d(data, target, target_names=None):
    '''Show data reduced to 2 dimensions as scatter plot.
    Colors mark the different labels.
    '''
    pca = PCA(n_components=2, whiten=True)
    compressed = pca.fit_transform(data)
    target_names = set(target) if target_names is None else target_names
    colors = cycle('rgbcmykw')
    target_ids = range(len(target_names))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for i, c, label in zip(target_ids, colors, target_names):
        ax.scatter(compressed[target == i, 0], compressed[target == i, 1],
                   c=c, label=label)
    ax.legend()
    return fig


if __name__ == '__main__':
    from sklearn.datasets import load_iris
    iris = load_iris()
    fig = plot2d(iris.data, iris.target, iris.target_names)
    plt.show()  # We use plt.show so it'll block until the image is closed
