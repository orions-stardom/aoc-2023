#!/usr/bin/env -S pdm run python
import itertools as it
from functools import reduce

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... 0 3 6 9 12 15
    ... 1 3 6 10 15 21
    ... 10 13 16 21 30 45
    ... ''')
    114
    """
    extrapolated = []
    for line in rawdata.splitlines():
        vals = [int(val) for val in line.split()]
        finals = [vals[-1]]
        while any(vals):
            vals = [b-a for a,b in it.pairwise(vals)]
            finals.append(vals[-1])

        extrapolated.append(sum(finals))
    return sum(extrapolated)

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... 0 3 6 9 12 15
    ... 1 3 6 10 15 21
    ... 10 13 16 21 30 45
    ... ''')
    2
    """
    extrapolated = []
    for line in rawdata.splitlines():
        vals = [int(val) for val in line.split()]
        firsts = [vals[0]]
        while any(vals):
            vals = [b-a for a,b in it.pairwise(vals)]
            firsts.append(vals[0])

        extrapolated.append(reduce(lambda extra,prev:prev-extra, reversed(firsts)))

    return sum(extrapolated)

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
