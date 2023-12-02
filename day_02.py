#!/usr/bin/env -S pdm run python

from dataclasses import dataclass
import re

@dataclass
class CubeSubset:
    """
    >>> CubeSubset("3 blue, 4 red")
    CubeSubset(blue=3, red=4, green=0)
    """
    blue: int 
    red: int 
    green: int

    def __init__(self, data:str):
        for colour in "red", "green", "blue":
            parsed = re.search(rf"(?P<count>\d+) {colour}", data)
            self.__dict__[colour] = int(parsed["count"]) if parsed else 0

def parse_games(data: str) -> dict[int, list[CubeSubset]]:
    def parse_game(line):
        id_, subset_data = re.fullmatch(r"Game (\d+): (.*)", line).groups()
        return int(id_), [CubeSubset(subset) for subset in subset_data.split(";")]

    return dict(parse_game(line) for line in data.splitlines())


def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    ... Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    ... Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    ... Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    ... Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green''')
    8
    """
    games = parse_games(rawdata)
    
    def is_possible(game):
        return all(subset.red <= 12 and subset.green <= 13 and subset.blue <= 14 for subset in game)

    return sum(id_ for id_,game in games.items() if is_possible(game))

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    ... Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    ... Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    ... Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    ... Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green''')
    2286
    """
    games = parse_games(rawdata)
    def minimum_power(game):
        return max(s.red for s in game) * max(s.green for s in game) * max(s.blue for s in game) 

    return sum(minimum_power(game) for game in games.values())

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
