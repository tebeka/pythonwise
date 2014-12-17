from operator import itemgetter
from itertools import imap, chain, repeat

def rotate(matrix):
  '''Rotate matrix 90 degrees'''
  def row(row_num):
      return map(itemgetter(row_num), matrix)

  return map(row, range(len(matrix[0])))

def stretch(items, times):
  '''stretch([1,2], 3) -> [1,1,1,2,2,2]'''
  return reduce(add, map(lambda item: [item] * times, items), [])

def istretch(items, count):
    '''istretch([1,2], 3) -> [1,1,1,2,2,2] (generator)'''
    return chain(*imap(lambda i: repeat(i, count), items))
