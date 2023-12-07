#!/usr/bin/env -S pdm run python

from enum import Enum
from dataclasses import dataclass
from collections import Counter
from typing import NamedTuple

@dataclass
class Card:
    value: str

    @property
    def numeric_value(self) -> int:
        if self.value.isdigit():
            return int(self.value)

        return "TJQKA".index(self.value) + 10

    def __lt__(self, other:"Card"):
        return self.numeric_value < other.numeric_value

    def __hash__(self):
        return hash(self.value)

class HandType(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    def __lt__(self, other:"HandType"):
        return self.value < other.value

    @staticmethod
    def type_of(hand: Counter[Card]):
        match hand.most_common():
            case [(_, 1),(_, 1),(_, 1),(_, 1),(_, 1)]:
                return HandType.HIGH_CARD
            case [(_,2),(_, 1),(_, 1),(_, 1)]:
                return HandType.PAIR
            case [(_,2), (_,2), (_,1)]:
                return HandType.TWO_PAIR
            case [(_,3),(_, 1),(_, 1)]:
                return HandType.THREE_OF_A_KIND
            case [(_,3),(_,2)]:
                return HandType.FULL_HOUSE
            case [(_,4),(_,1)]:
                return HandType.FOUR_OF_A_KIND
            case [(_,5)]:
                return HandType.FIVE_OF_A_KIND

type Hand = tuple[HandType, Card, Card, Card, Card, Card]

class Play(NamedTuple):
    hand: Hand
    bet: int

    @classmethod
    def parse(cls, data:str):
        hand_data,bet_data = data.split()
        cards = [Card(c) for c in hand_data]
        hand = (HandType.type_of(Counter(hand_data)), *cards)
        return cls(hand, int(bet_data))

    @classmethod
    def parse_with_jokers(cls, data:str):
        hand_data,bet_data = data.split()

        # replace all the Jokers with 1s so they compare properly
        cards = [Card(c) for c in hand_data.replace("J", "1")]

        joker = Card("1")
        count = Counter(cards)
        n_jokers = count[joker]

        if n_jokers == 5:
            # if all the cards are jokers then.. its just 5 jokers
            hand = (HandType.FIVE_OF_A_KIND, joker, joker, joker, joker, joker)
        else:
            # otherwise the jokers become the most commor non-joker card
            # breaking ties with face value
            del count[joker]
            best = max((n,val) for val,n in count.most_common())[1]
            count[best] += n_jokers 
            hand = (HandType.type_of(count), *cards)

        return cls(hand, int(bet_data))

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... 32T3K 765
    ... T55J5 684
    ... KK677 28
    ... KTJJT 220
    ... QQQJA 483
    ... ''')
    6440
    """
    plays = sorted(Play.parse(line) for line in rawdata.splitlines())
    return sum(i*play.bet for i,play in enumerate(plays, start=1))

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... 32T3K 765
    ... T55J5 684
    ... KK677 28
    ... KTJJT 220
    ... QQQJA 483
    ... ''')
    5905
    """
    plays = sorted(Play.parse_with_jokers(line) for line in rawdata.splitlines())
    return sum(i*play.bet for i,play in enumerate(plays, start=1))

if __name__ == "__main__":
    import aocd
    import doctest
    import sys
     
    failure, tests = doctest.testmod()
    if failure > 0:
        sys.exit(f"Failed {failure}/{tests} tests")
   
    # aocd has some magic introspection but it doesnt like my naming conventions
    from pathlib import Path
    f = Path(__file__)
    puzzle_input = aocd.get_data(
        year=f.parent.name.removeprefix("aoc-"),
        day=int(f.stem.removeprefix("day_")))
    
    for part in 1, 2:
        try:
            impl = globals()[f"part_{part}"]
        except KeyError:
            print(f"No part {part} - skipping")
            continue

        solution = impl(puzzle_input)
        if solution is not None:
            print(f"Solution to part {part}: ", solution, sep="\n")
            # aocd uses parts a and b for some reason, even though AOC uses parts One and Two
            aocd.submit(solution, part='ab'[part-1], reopen=False)
        else:
            print("No solution to part {part} {might need to be entered manually?)")
