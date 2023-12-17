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
    lines = s.splitlines()
    times = support.parse_numbers_split(lines[0].split(":")[1])
    dist = support.parse_numbers_split(lines[1].split(":")[1])

    possibilities = [0] * len(times)
    for i in range(len(times)):
        t = times[i]
        d = dist[i]

        for x in range(t):
            if x*(t-x) > d:
                possibilities[i] += 1
    return math.prod(possibilities)


INPUT_S = '''\
Time:      7  15   30
Distance:  9  40  200
'''
EXPECTED = 288


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
