#!/usr/bin/env -S pdm run python
import numpy as np

def find_reflection(vector, differences=0):
    size = vector.shape[0]
    midpoint = size/2
    for test in range(1,size):
        # check for reflection along the line between (test-1) and test
        if test <= midpoint:
            lhs, rhs = vector[:test],vector[test:2*test]
        if test > midpoint:
            delta = size - test
            lhs,rhs = vector[(test-delta):test],vector[test:test+delta]   

        if (lhs != rhs[::-1]).sum() == differences:
            return test

    return 0

def count_reflections(notes:str, differences=0):
    pattern = np.array([list(line) for line in notes.splitlines()])
    row_result = find_reflection(pattern, differences)
    col_result = find_reflection(pattern.T, differences)
    return 100*row_result + col_result

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... #.##..##.
    ... ..#.##.#.
    ... ##......#
    ... ##......#
    ... ..#.##.#.
    ... ..##..##.
    ... #.#.##.#.
    ... 
    ... #...##..#
    ... #....#..#
    ... ..##..###
    ... #####.##.
    ... #####.##.
    ... ..##..###
    ... #....#..#
    ... ''')
    405
    """
    return sum(count_reflections(notes) for notes in rawdata.split("\n\n"))

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... #.##..##.
    ... ..#.##.#.
    ... ##......#
    ... ##......#
    ... ..#.##.#.
    ... ..##..##.
    ... #.#.##.#.
    ... 
    ... #...##..#
    ... #....#..#
    ... ..##..###
    ... #####.##.
    ... #####.##.
    ... ..##..###
    ... #....#..#
    ... ''')
    400
    """
    return sum(count_reflections(notes, differences=1) for notes in rawdata.split("\n\n"))

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
