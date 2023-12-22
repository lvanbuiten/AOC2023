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
    total = 0
    for line in s.splitlines():
        todo = [support.parse_numbers_split(line)]
        final_nrs = []
        while len(todo) > 0:
            nrs = todo.pop()
            final_nrs.append(nrs[-1])
            
            new_todo = []
            for i in range(len(nrs)-1):
                new_todo.append(nrs[i+1] - nrs[i])

            if not all(x == 0 for x in new_todo):
                todo.append(new_todo)

        for i in range(len(final_nrs)-1, 0, -1):
            final_nrs[i-1] += final_nrs[i]

        total += final_nrs[0]

    return total


INPUT_S = '''\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''
EXPECTED = 114


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
