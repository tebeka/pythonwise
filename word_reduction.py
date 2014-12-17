#!/usr/bin/env python
# A little solution to http://ddj.com/cpp/202806370?pgno=3
# Works fast enough as well (running on http://www.gutenberg.org/etext/3201)
# $ time ./word_reduction.py dictionaries/SINGLE.TXT
# restraint's
# restraints
# restrains
# retrains
# retains
# retain
# retin
# rein
# rin
# in
# n
# 
# real    0m4.088s
# user    0m4.023s
# sys     0m0.065s

DICTIONRAY = set()

def load_dictionary(filename):
  DICTIONRAY.add("a")
  DICTIONRAY.add("i")
  for line in open(filename):
      DICTIONRAY.add(line.strip())

def _reduction(word):
  if word not in DICTIONRAY:
      return []
  if len(word) == 1:
      return [word]

  for i in range(len(word)):
      subword = "%s%s" % (word[:i], word[i+1:])
      if subword not in DICTIONRAY:
          continue
      path = reduction(subword)
      if path:
          return [word] + path
  return []

CACHE = {}
def reduction(word):
  if word not in CACHE:
      CACHE[word] = _reduction(word)

  return CACHE[word]

def main(argv=None):
  if argv is None:
      import sys
      argv = sys.argv

  from os.path import isfile
  from optparse import OptionParser

  parser = OptionParser("usage: %prog DICTIONRAY")

  opts, args = parser.parse_args(argv[1:])
  if len(args) != 1:
      parser.error("wrong number of arguments") # Will exit

  dictfile = args[0]
  if not isfile(dictfile):
      raise SystemExit("error: can't find %s" % dictfile)

  load_dictionary(dictfile)
  for word in sorted(DICTIONRAY, key=lambda w: len(w), reverse=1):
      path = reduction(word)
      if path:
          print "\n".join(path)
          break

if __name__ == "__main__":
  main()
