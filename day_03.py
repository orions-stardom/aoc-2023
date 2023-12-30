#!/usr/bin/env -S pdm run python
import parse
import itertools as it
from collections import defaultdict
import math

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... 467..114..
    ... ...*......
    ... ..35..633.
    ... ......#...
    ... 617*......
    ... .....+.58.
    ... ..592.....
    ... ......755.
    ... ...$.*....
    ... .664.598..
    ... ''')
    4361
    """
    data = rawdata.splitlines()
    parts_found = []
    width, height = len(data[0]), len(data)
    for lineno, line in enumerate(data):
        for res in parse.findall("{:d}", line):
            number = abs(res.fixed[0])

            start_col, end_col = res.spans[0]

            for x,y in it.product(range(start_col-1,end_col+1),(lineno-1,lineno,lineno+1)):
                if 0 <= x < width and 0 <= y < height:
                    c = data[y][x]
                    if not c.isdigit() and c != ".":
                        parts_found.append(number)
                        break
    return sum(parts_found)

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... 467..114..
    ... ...*......
    ... ..35..633.
    ... ......#...
    ... 617*......
    ... .....+.58.
    ... ..592.....
    ... ......755.
    ... ...$.*....
    ... .664.598..
    ... ''')
    467835
    """
    data = rawdata.splitlines()
    gears_found = defaultdict(list)

    width, height = len(data[0]), len(data)
    for lineno, line in enumerate(data):
        for res in parse.findall("{:d}", line):
            number = abs(res.fixed[0])
            start_col, end_col = res.spans[0]

            for x,y in it.product(range(start_col-1,end_col+1),(lineno-1,lineno,lineno+1)):
                if 0 <= x < width and 0 <= y < height:
                    if data[y][x] == "*":
                        gears_found[(x,y)].append(number)
                        
    return sum(math.prod(parts) for parts in gears_found.values() if len(parts) == 2)

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
