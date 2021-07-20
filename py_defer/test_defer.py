from subprocess import Popen

import pytest


@pytest.fixture
def defer():
    funcs = []

    yield funcs

    for fn in reversed(funcs):
        try:
            fn()
        except Exception as err:
            print(f'error: {err}')


def test_kill(defer):
    p = Popen(['sleep', '1000'])  # simulate server
    print(p.pid)
    defer.append(p.kill)
