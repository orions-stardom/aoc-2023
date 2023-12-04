#!/usr/bin/env -S pdm run python
from dataclasses import dataclass
from collections import Counter
import re

@dataclass
class Card:
    id_: int
    winning_numbers: list[int]
    selected_numbers: list[int]
    matches: int

    def __init__(self, data:str):
        id_, winning, selected = re.fullmatch(r"Card\s+(\d+)\s*:([\d\s]+)\|([\d\s]+)", data).groups()
        self.id_ = int(id_)
        self.winning_numbers = [int(n) for n in winning.split()]
        self.selected_numbers = [int(n) for n in selected.split()]

        self.matches = sum(number in self.winning_numbers for number in self.selected_numbers)


def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    ... Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    ... Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    ... Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    ... Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    ... Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    ... ''')
    13
    """
    cards = [Card(line) for line in rawdata.splitlines()]
    return sum(2**(card.matches-1) for card in cards if card.matches)

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    ... Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    ... Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    ... Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    ... Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    ... Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    ... ''')
    30
    """
    cards = [Card(line) for line in rawdata.splitlines()]
    count = Counter(card.id_ for card in cards)
    for i, card in enumerate(cards):
        current_count = count[card.id_]
        for j in range(1, card.matches+1):
            if i+j < len(cards):
                count[cards[i+j].id_] += current_count

    return count.total()


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
