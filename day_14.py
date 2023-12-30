#!/usr/bin/env -S pdm run python
import itertools as it
import more_itertools as mit
import functools

@functools.cache
def tilt(rocks: tuple[str]) -> tuple[str]:
    # tilt north
    res = []
    for col in zip(*rocks):
        resulting_col = []
        for k, group in it.groupby(col, lambda k: k == "#"):
            if k:
                resulting_col.extend(group)
            else:
                empty, move = mit.partition(lambda r: r == "O", group) 
                resulting_col.extend(move)
                resulting_col.extend(empty)

        res.append("".join(resulting_col))
    return tuple("".join(row) for row in zip(*res))

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... O....#....
    ... O.OO#....#
    ... .....##...
    ... OO.#O....O
    ... .O.....O#.
    ... O.#..O.#.#
    ... ..O..#O..O
    ... .......O..
    ... #....###..
    ... #OO..#....
    ... ''')
    136
    """
    data = rawdata.splitlines()
    return total_load(tilt(tuple(data)))

@functools.cache
def spincycle(rocks: tuple[str]) -> tuple[str]:
    rocks = tilt(rocks)
    for _ in range(3):
        rocks = tuple(r[::-1] for r in zip(*rocks))
        rocks = tilt(rocks)

    rocks = tuple("".join(r[::-1]) for r in zip(*rocks))
    return rocks

def total_load(rocks : tuple[str]) -> int:
    rows = len(rocks)
    return sum(rows-i for col in zip(*rocks) for i,r in enumerate(col) if r=="O")

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... O....#....
    ... O.OO#....#
    ... .....##...
    ... OO.#O....O
    ... .O.....O#.
    ... O.#..O.#.#
    ... ..O..#O..O
    ... .......O..
    ... #....###..
    ... #OO..#....
    ... ''')
    64
    """
    rocks = tuple(rawdata.splitlines())
    # FIXME I just picked this number from nowhere and it seemed to work..
    # would rather have the program work it out somehow.. but even with cacheing
    # 1_000_000_000 wasnt going to finish even on the example
    for _ in range(1_000): 
        rocks = spincycle(rocks)

    return total_load(rocks)

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
