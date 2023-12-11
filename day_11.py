#!/usr/bin/env -S pdm run python
import numpy as np
import itertools as it

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... ...#......
    ... .......#..
    ... #.........
    ... ..........
    ... ......#...
    ... .#........
    ... .........#
    ... ..........
    ... .......#..
    ... #...#.....
    ... ''')
    374
    """
    data = np.array([[c=="#" for c in line] for line in rawdata.splitlines()])

    empty_cols = np.where(~data.any(axis=0))[0]
    empty_rows = np.where(~data.any(axis=1))[0]

    galaxies = list(zip(*data.nonzero()))

    def taxicab(x1,y1,x2,y2):
        return abs(x1-x2)+abs(y1-y2)+sum(x1 < x < x2 or x2 < x < x1 for x in empty_rows) + sum(y1 < y < y2  or y2 < y < y1 for y in empty_cols)

    # breakpoint()
    return sum(taxicab(*p1,*p2) for p1,p2 in it.combinations(galaxies,2))

def part_2(rawdata, expansion_factor=1_000_000):
    r"""
    >>> part_2('''\
    ... ...#......
    ... .......#..
    ... #.........
    ... ..........
    ... ......#...
    ... .#........
    ... .........#
    ... ..........
    ... .......#..
    ... #...#.....
    ... ''', 10)
    1030

    >>> part_2('''\
    ... ...#......
    ... .......#..
    ... #.........
    ... ..........
    ... ......#...
    ... .#........
    ... .........#
    ... ..........
    ... .......#..
    ... #...#.....
    ... ''', 100)
    8410
    """
    data = np.array([[c=="#" for c in line] for line in rawdata.splitlines()])

    empty_cols = np.where(~data.any(axis=0))[0]
    empty_rows = np.where(~data.any(axis=1))[0]

    galaxies = list(zip(*data.nonzero()))

    def taxicab(x1,y1,x2,y2):
        return abs(x1-x2)+abs(y1-y2)+sum(x1 < x < x2 or x2 < x < x1 for x in empty_rows)*(expansion_factor-1) + sum(y1 < y < y2  or y2 < y < y1 for y in empty_cols)*(expansion_factor-1)

    # breakpoint()
    return sum(taxicab(*p1,*p2) for p1,p2 in it.combinations(galaxies,2))
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
