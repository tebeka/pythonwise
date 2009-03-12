#!/usr/bin/env python

from functools import partial
import re

filter_comment = partial(re.compile("#.*$").sub, "")
words = re.compile("[^ \t\n\r]+").findall

def num_words(text):
  '''Return the number of words in a code segment, ignoring comments

  >>> num_words("")
  0
  >>> num_words("1 + 1")
  3
  >>> num_words("1 + 1 # add 1 to 1")
  3
  '''
  return sum(map(len,
                 map(words,
                     map(filter_comment,
                         text.splitlines()))))


if __name__ == "__main__":
  import doctest
  doctest.testmod()
