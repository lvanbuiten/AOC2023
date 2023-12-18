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
    seeds, *steps = s.split('\n\n')
    seedsS = seeds.split(': ')[1].split()
    map = {}
    for i,step in enumerate(steps):
        map[i] = list()
        for n in step.splitlines()[1::]:
            drs, srs, rl = support.parse_numbers_split(n) # destination range start, source range start, range length
            map[i].append((drs, srs, rl))

    seeds = []
    for i in range(0, len(seedsS), 2):
        s = int(seedsS[i])
        r = int(seedsS[i+1])
        seeds.append((s, s+r))

    for m in map:
        new_seeds = []
        while len(seeds) > 0:
            start, end = seeds.pop()
            for drs, srs, rl in map[m]:
                max_start = max(start, srs)
                min_end = min(end, srs+rl)
                
                if max_start < min_end:
                    # found overlap
                    new_seeds.append((
                        drs + (max_start-srs), 
                        drs + min_end-srs
                    ))

                    # add undetermined seeds
                    if start < max_start:
                        seeds.append((start, max_start))
                    if min_end < end:
                        seeds.append((min_end, end))

                    break
            else:
                # no overlap, add as is
                new_seeds.append((start, end))

        seeds = new_seeds #next map or final results
    return min(seeds)[0]


INPUT_S = '''\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''
EXPECTED = 46


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
