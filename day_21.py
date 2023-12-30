#!/usr/bin/env -S pdm run python
import numpy as np
import itertools as it

def part_1(rawdata, steps=64):
    r"""
    >>> part_1('''\
    ... ...........
    ... .....###.#.
    ... .###.##..#.
    ... ..#.#...#..
    ... ....#.#....
    ... .##..S####.
    ... .##..#...#.
    ... .......##..
    ... .##.#.####.
    ... .##..##.##.
    ... ...........
    ... ''', steps=6)
    16
    """
    data = {complex(x,y) for y, line in enumerate(rawdata.splitlines()) for x, c in enumerate(line) if c != "#"}
    # S is always in the dead center
    start = complex((max(z.real for z in data)+1) // 2 , (max(z.imag for z in data)+1)//2)

    destinations = {start}
    directions = 1j, -1j, 1, -1
    for step in range(steps):
        destinations = set(w for z in destinations for dz in directions if (w:=z+dz) in data)
    return len(destinations)

def part_2(rawdata, steps=26501365):
    r"""
    # >>> part_2('''\
    # ... ...........
    # ... .....###.#.
    # ... .###.##..#.
    # ... ..#.#...#..
    # ... ....#.#....
    # ... .##..S####.
    # ... .##..#...#.
    # ... .......##..
    # ... .##.#.####.
    # ... .##..##.##.
    # ... ...........
    # ... ''', steps=500)
    # 167004
    """
    data = {complex(x,y) for y, line in enumerate(rawdata.splitlines()) for x, c in enumerate(line) if c != "#"}
    w, h = int(max(z.real for z in data)+1), int(max(z.imag for z in data)+1)
    assert w==h
    # S is always in the dead center
    start = complex(w//2 , h//2)

    destinations = {start}
    p1_destinations = {start}
    # if f(n) is the number of places we can each after n steps, then (apparently)
    # this can be interpolated using a Newton polynomial with 3 x-values spaced one grid width apart 
    directions = 1j, -1j, 1, -1
    x = (steps%w, steps%w+w, steps%w+2*w)
    y = []
    for xn in it.count(1):
        destinations = set(z+dz for z in destinations for dz in directions if complex((z.real+dz.real)%w, (z.imag+dz.imag)%h) in data)
        if xn in x:
            y.append(len(destinations))
        if len(y) == len(x):
            break
    
    a0 = y[0]
    a1 = y[1] - y[0]
    a2 = y[2] - y[1] 
    n = steps//w
    return a0+a1*n+(n*(n-1)//2)*(a2-a1)

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
