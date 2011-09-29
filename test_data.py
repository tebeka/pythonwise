# Example on how to use generators with nose for data driven tests

def check_mul(a, b, result):
    assert a * b == result, "{0}*{1} != {2}".format(a, b, result)

def test_mul():
    cases = [
        [2, 2, 4],
        [-2, 2, -4],
        [0.1, 10, 1],
    ]
    for a, b, result in cases:
        yield check_mul, a, b, result

