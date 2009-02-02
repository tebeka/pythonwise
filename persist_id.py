#!/usr/bin/env python
# Persistant ID generator

from collections import defaultdict
from itertools import count

vector_index = defaultdict(count(0).next)
print vector_index["a"] # 0
print vector_index["a"] # 0
print vector_index["b"] # 1
