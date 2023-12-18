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

    pos = []
    mappings = {}
    for m in mapS.splitlines():
        k,v = m.split(' = ')
        mappings[k] = tuple(v[1:-1].split(', '))

        if k[-1] == 'A':
            pos.append(k)

    counts = []
    print(pos)
    for p in pos:
        cur = p
        i = 0
        while(True):
            if cur.endswith('Z'):
                counts.append(i)
                break

            cur = mappings[cur][int(lrSteps[i % lrLen])]
            i += 1
    print(counts)
    return math.lcm(*counts)


INPUT_S = '''\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
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
