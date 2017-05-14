"""Base class for creating scikit-learn Pipeline compatible steps"""

from abc import ABC, abstractmethod


class Step(ABC):
    """Step in pipeline.

    You *must* override "transform"
    """

    @abstractmethod
    def transform(self, df, y=None):
        """Transform a DataFrame"""
        pass

    # API compatibility
    def fit(X, y, sample_weight=None):
        pass

    def get_params(self, deep=False):
        return vars(self)

    def set_params(self, **kw):
        self.__dict__.update(**kw)


# Example Usage

class Sampler(Step):
    """Sample data frame"""
    def __init__(self, frac, random_state=None):
        self.frac = frac
        self.random_state = random_state

    def transform(self, df, y=None):
        df = df.sample(frac=self.frac, random_state=self.random_state)
        return df.copy()


class ColMul(Step):
    """Multiply column by constant"""
    def __init__(self, col, val):
        self.col = col
        self.val = val

    def transform(self, df, y=None):
        df = df.copy()
        df[self.col] = df[self.col] * self.val
        return df

# Example Usage
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('sample', Sampler(0.2)),
    ('mul_z', ColMul('z', 100)),
])

pipe.set_params(sample__random_state=17)

df = pd.DataFrame(np.random.rand(100, 3), columns=['x', 'y', 'z'])
print(pipe.transform(df))
