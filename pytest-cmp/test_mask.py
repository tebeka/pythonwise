import pytest
from os.path import abspath, dirname
import toml

from mask import mask

here = dirname(abspath(__file__))


def iter_mask_cases():
    with open(f'{here}/mask_cases.toml') as fp:
        cfg = toml.load(fp)
        for case in cfg['mask_cases']:
            # id sets the test name being printed out
            yield pytest.param(case['in'], case['out'], id=case['id'])


@pytest.mark.parametrize('text, expected', iter_mask_cases())
def test_mask(text, expected):
    out = mask(text)
    assert out == expected
