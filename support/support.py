from __future__ import annotations

import argparse
import contextlib
import enum
import os.path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Generator

HERE = os.path.dirname(os.path.abspath(__file__))


@contextlib.contextmanager
def timing(name: str = '') -> Generator[None, None, None]:
    before = time.time()
    try:
        yield
    finally:
        after = time.time()
        t = (after - before) * 1000
        unit = 'ms'
        if t < 100:
            t *= 1000
            unit = 'μs'
        if name:
            name = f' ({name})'
        print(f'> {int(t)} {unit}{name}', file=sys.stderr, flush=True)


def adjacent_4(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    yield x, y - 1
    yield x + 1, y
    yield x, y + 1
    yield x - 1, y

def adjacent_4_in_range(x: int, y: int, maxX: int, maxY: int) -> Generator[tuple[int, int], None, None]:
    if y > 0:
        yield x, y - 1
    if x < maxX:
        yield x + 1, y
    if y < maxY:
        yield x, y + 1
    if x > 0:
        yield x - 1, y

def adjacent_8(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    for y_d in (-1, 0, 1):
        for x_d in (-1, 0, 1):
            if y_d == x_d == 0:
                continue
            yield x + x_d, y + y_d

def adjacent_8_including(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    for y_d in (-1, 0, 1):
        for x_d in (-1, 0, 1):
            yield x + x_d, y + y_d


def parse_coords_int(s: str) -> dict[tuple[int, int], int]:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = int(c)
    return coords


def parse_coords_hash(s: str) -> set[tuple[int, int]]:
    coords = set()
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                coords.add((x, y))
    return coords


def parse_numbers_split(s: str) -> list[int]:
    return [int(x) for x in s.split()]


def parse_numbers_comma(s: str) -> list[int]:
    return [int(x) for x in s.strip().split(',')]


def format_coords_hash(coords: set[tuple[int, int]]) -> str:
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)
    return '\n'.join(
        ''.join(
            '#' if (x, y) in coords else ' '
            for x in range(min_x, max_x + 1)
        )
        for y in range(min_y, max_y + 1)
    )

def format_coords_hash_values(coords: dict) -> str:
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)
    return '\n'.join(
        ''.join(
            coords.get((x,y), '.')
            for x in range(min_x, max_x + 1)
        )
        for y in range(min_y, max_y + 1)
    )

def print_coords_hash(coords: set[tuple[int, int]]) -> None:
    print(format_coords_hash(coords))


class Direction4(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    @property
    def _vals(self) -> tuple[Direction4, ...]:
        return tuple(type(self).__members__.values())

    @property
    def cw(self) -> Direction4:
        vals = self._vals
        return vals[(vals.index(self) + 1) % len(vals)]

    @property
    def ccw(self) -> Direction4:
        vals = self._vals
        return vals[(vals.index(self) - 1) % len(vals)]

    @property
    def opposite(self) -> Direction4:
        vals = self._vals
        return vals[(vals.index(self) + 2) % len(vals)]

    def apply(self, x: int, y: int, *, n: int = 1) -> tuple[int, int]:
        return self.x * n + x, self.y * n + y
