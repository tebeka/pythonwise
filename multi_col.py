"""Timeiming mulitple column query in Pandas DataFrame"""
from timeit import timeit
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string

np.random.seed(17)  # Repeatable results


def rand_letters(size):
    return np.random.choice(list(string.ascii_lowercase), size)


def new_df(size):
    return pd.DataFrame({
        'x': rand_letters(size),
        'y': rand_letters(size),
        'z': rand_letters(size),
    })


def iter_filter(df, pred):
    """Filter with iteration"""
    mask = pd.Series([True] * len(df))
    for col, val in pred:
        mask &= (df[col] == val)
    return df[mask]


def merge_filter(df, pred):
    """Filter with merge"""
    cols, values = [p[0] for p in pred], [p[1] for p in pred]
    jdf = pd.DataFrame([values], columns=cols)
    return df.reset_index().merge(jdf, on=cols).set_index('index')


def query_filter(df, pred):
    """Query with df.query"""
    query = '&'.join(f'{col}=={val!r}' for col, val in pred)
    return df.query(query)


ntimes = 1_000

pred = [
    ('x', 'z'),
    ('y', 'g'),
]

data = []

for size in (1_000, 10_000, 100_000):
    df = new_df(size)
    for fn in (iter_filter, merge_filter, query_filter):
        fname = fn.__name__
        runtime = timeit(
            f'{fname}(df, pred)',
            f'from __main__ import df, pred, {fname}',
            number=ntimes)
        time = runtime / ntimes
        data.append([size, fn.__name__, time])

# Plot results

tdf = pd.DataFrame(data, columns=['size', 'name', 'time'])
# query_filter -> query
tdf['name'] = tdf['name'].str.replace('_filter', '')

plt.style.use('seaborn-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

ax1 = None
for i, (key, sdf) in enumerate(tdf.groupby('size'), 1):
    ax = plt.subplot(1, 3, i, title=f'size={key:,}', sharey=ax1)
    sdf['time'].plot.bar(ax=ax)
    ax.set_xticklabels(sdf['name'], rotation='horizontal')
    ax1 = ax1 or ax

plt.gcf().savefig('multi_col.png')
