from __future__ import annotations
from __future__ import absolute_import

import argparse
import os
import sys
import string
import collections
import math
from typing import NamedTuple
from enum import Enum
from functools import cmp_to_key

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support import support

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class HandRank(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7

class Hand(NamedTuple):
    cards: str
    bid: int
    cardsValue: HandRank

    @classmethod
    def parse(cls, s: str) -> Hand:
        cards, bid = s.split()

        hasJokers = False
        hand = {'A': 0, 'K': 0, 'Q': 0, 'J': 0, 'T': 0, '9': 0, '8': 0, '7': 0, '6': 0, '5': 0, '4': 0, '3': 0, '2': 0}
        for c in cards:
            if c == 'J':
                hasJokers = True
                continue
            hand[c] +=1

        if hasJokers:
            highestKey = max(hand, key=hand.get)
            for c in cards:
                if c == 'J':
                    hand[highestKey] += 1

        cardsValue = HandRank.HIGH_CARD
        if (5 in hand.values()):
            cardsValue = HandRank.FIVE_OF_A_KIND
        elif (4 in hand.values()):
            cardsValue = HandRank.FOUR_OF_A_KIND
        elif (all(x in hand.values() for x in [3,2])):
            cardsValue = HandRank.FULL_HOUSE
        elif (3 in hand.values()):
            cardsValue = HandRank.THREE_OF_A_KIND
        elif (2 == len([x for x in hand.values() if x == 2])):
            cardsValue = HandRank.TWO_PAIR
        elif (2 in hand.values()):
            cardsValue = HandRank.ONE_PAIR

        return cls(cards, int(bid), cardsValue)

def compare(self: Hand, other: Hand):
    if (self.cardsValue.value < other.cardsValue.value):
        return 1
    if (self.cardsValue.value > other.cardsValue.value):
        return -1

    for i in range(5):
        cardRank = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
        c = cardRank.index(self.cards[i])
        oc = cardRank.index(other.cards[i])

        if (c < oc):
            return 1
        if (c > oc):
            return -1
        
    raise NotImplementedError('unreachable')

def compute(s: str) -> int:
    hands = [Hand.parse(line) for line in s.splitlines()]
    hands.sort(key=cmp_to_key(compare))

    return sum([(i+1)*h.bid for i,h in enumerate(hands)])


INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 5905


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
