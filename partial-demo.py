#!/usr/bin/env python

from functools import partial
import re
remove_prefix = partial(re.compile("prefix: ").sub, "")
print remove_prefix("prefix: hello") # 'hello'
print remove_prefix("hello") # 'hello'
