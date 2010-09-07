from collections import deque

def ilast(col, N):
    "Get last N items in collection"
    return deque(iter(col), N)
