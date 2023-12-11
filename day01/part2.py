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

number_replacements = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def compute(s: str) -> int:
    total = 0
    regex = re.compile(fr'(\d|{"|".join(number_replacements)}).*')
    regex_rev = re.compile(fr'.*(\d|{"|".join(number_replacements)})')
    lines = s.splitlines()
    for line in lines:
        first = regex.search(line).group(1)
        last = regex_rev.search(line).group(1)
        total += int(number_replacements.get(first, first) + number_replacements.get(last, last))
    return total


INPUT_S = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''
EXPECTED = 281


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
