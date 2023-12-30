#!/usr/bin/env -S pdm run python

from enum import Enum
from dataclasses import dataclass
from collections import Counter
import parse

@dataclass
class Card:
    value: str
    numeric_value: int

    def __init__(self, face_value:str):
        self.value = face_value
        if face_value.isdigit():
            self.numeric_value = int(self.value)
        else:
            self.numeric_value = "TJQKA".index(self.value) + 10

    def __lt__(self, other:"Card"):
        return self.numeric_value < other.numeric_value

    def __hash__(self):
        return hash(self.value)

joker = Card("J")
joker.numeric_value = 1

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

@dataclass(order=True)
class Hand:
    hand_type: HandType
    cards: list[Card]

    def __init__(self, cards:list[Card]):
        self.cards = cards

        # if all the cards are jokers.. thats just five jokers,
        # so we skip all the shenanigans
        if cards == [joker,joker,joker,joker,joker]:
            self.hand_type = HandType.FIVE_OF_A_KIND
            return

        # otherwise we find the other card we have the most of (breaking ties with the card value)
        # and treat the jokers as that for the purpose of figuring out the hand type
        count = Counter(card for card in cards if card != joker)
        n_jokers = 5 - count.total()
        count[max(count, key=count.get)] += n_jokers

        match count.most_common():
            case [(_, 1),(_, 1),(_, 1),(_, 1),(_, 1)]:
                self.hand_type = HandType.HIGH_CARD
            case [(_,2),(_, 1),(_, 1),(_, 1)]:
                self.hand_type = HandType.PAIR
            case [(_,2), (_,2), (_,1)]:
                self.hand_type = HandType.TWO_PAIR
            case [(_,3),(_, 1),(_, 1)]:
                self.hand_type = HandType.THREE_OF_A_KIND
            case [(_,3),(_,2)]:
                self.hand_type = HandType.FULL_HOUSE
            case [(_,4),(_,1)]:
                self.hand_type = HandType.FOUR_OF_A_KIND
            case [(_,5)]:
                self.hand_type = HandType.FIVE_OF_A_KIND

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
    @parse.with_pattern(r"[2-9TJKQA]{5}")
    def parse_hand(data:str):
        return Hand([Card(c) for c in data])

    plays = sorted(tuple(play) for play in parse.findall("{:hand} {:d}", rawdata, extra_types={"hand":parse_hand}))
    return sum(i*bet for i,(_,bet) in enumerate(plays, start=1))

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
    @parse.with_pattern(r"[2-9TJKQA]{5}")
    def parse_hand(data:str):
        return Hand([Card(c) if c != "J" else joker for c in data])

    plays = sorted(tuple(play) for play in parse.findall("{:hand} {:d}", rawdata, extra_types={"hand":parse_hand}))
    return sum(i*bet for i,(_,bet) in enumerate(plays, start=1))

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
    year=f.parent.name.removeprefix("aoc-")
    day=int(f.stem.removeprefix("day_"))
    puzzle_input = aocd.get_data(year=year, day=day)
    
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
            aocd.submit(solution,part='ab'[part-1], day=day, year=year, reopen=False)
        else:
            print("No solution to part {part} {might need to be entered manually?)")
