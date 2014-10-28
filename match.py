#!/usr/bin/env python

# Support search syntax
'''
>>> match("a", "a")
True
>>> match("a", "")
False
>>> match("a AND b", "a c b")
True
>>> match("a AND b", "a c")
False
>>> match("NOT ( a OR b )", "z")
True
>>> match("a OR b", "b")
True
'''

def is_operator(token):
  return token in set(["and", "not", "or", "(", ")"])

def should_insert_and(expr, token):
  if not expr:
      return 0

  if is_operator(expr[-1]):
      return 0

  if is_operator(token):
      return 0

  return 1

def match(query, text):
  words = set(text.lower().split())

  expr = []
  for token in query.lower().split():

      if should_insert_and(expr, token):
          expr.append("and")

      if is_operator(token):
          expr.append(token)
      else:
          expr.append(token in words)

  py_expr = " ".join(map(str, expr))
  return eval(py_expr)

if __name__ == "__main__":
    from doctest import testmod
    testmod()
