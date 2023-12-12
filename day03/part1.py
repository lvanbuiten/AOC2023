from __future__ import annotations
from __future__ import absolute_import

import argparse
import os
import sys
import string
import collections
import math
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def is_symbol(s: str) -> bool:
    return not(s.isdigit() or s == '.')

def compute(s: str) -> int:
    lines = s.splitlines()
    maxY = len(lines)
    maxX = len(lines[0])
    sym_coords = set()
    num_seen = set()
    
    reg = re.compile('\\d+')
    num_coords = {} # coords to number keys 'i'
    num_values = {} # key to actual number value
    key_index = 0
    for y, line in enumerate(lines):
        for r in reg.finditer(line):
            key_index += 1
            num_values[key_index] = r.group()
            for i in range(*r.span()):
                num_coords[(i, y)] = key_index

        for x, c in enumerate(line):
            if is_symbol(c):
                sym_coords.add((x, y))

    for sym in sym_coords:
        for c in support.adjacent_8_in_range(sym[0], sym[1], maxX, maxY):
            # is a number and key is not in seen yet
            if (c in num_coords and num_coords.get(c) not in num_seen):
                num_seen.add(num_coords.get(c))
    return sum([int(num_values[key]) for key in num_seen])


INPUT_S = '''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''
EXPECTED = 4361


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
