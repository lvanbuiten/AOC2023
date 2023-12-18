from __future__ import annotations
from __future__ import absolute_import

import argparse
import os
import sys
import string
import collections
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lrString, mapS = s.split('\n\n')
    lrSteps = lrString.replace('L','0').replace('R','1')
    lrLen = len(lrSteps)

    mappings = {}
    for m in mapS.splitlines():
        k,v = m.split(' = ')
        mappings[k] = tuple(v[1:-1].split(', '))

    i = 0
    c = 'AAA'
    t = 'ZZZ'
    while(True):
        if (c == t):
            break
        c = mappings[c][int(lrSteps[i % lrLen])]
        i += 1

    return i


INPUT_S = '''\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''
EXPECTED = 6


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
