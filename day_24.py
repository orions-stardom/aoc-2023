#!/usr/bin/env -S pdm run python
import itertools as it
import math

def intersect_in_square(p0, v0, p1, v1, lo, hi):
    '''
    True if the lines defined by (p0, v0) and (p1, v1) where p is position at time 0 and v is velocity
    intersect within the square defined by x and y in (lo, hi)

    '''
    # We have two lines defined in parametric form so their interesection is at
    #    (x0,y0) + t(dx0,dy0) = (x1, y1) + s(dx1, dy1)

    # adapted from https://stackoverflow.com/a/41798064/779200

    d = v0.real*v1.imag - v0.imag*v1.real
    if math.isclose(d, 0):
        # vectors are parallel
        return False

    t = (v1.imag * (p1.real - p0.real) - v1.real * (p1.imag - p0.imag)) / d
    s = (v0.imag * (p1.real - p0.real) - v0.real * (p1.imag - p0.imag)) / d

    intersection = p0 + v0*t

    return (lo <= intersection.real <= hi) and (lo <= intersection.imag <= hi) and t > 0 and s > 0

    
def parse(line:str) -> tuple[complex,complex]:
    p_data, v_data = line.split(" @ ")
    p = complex(*map(int, p_data.split(", ")[:2]))
    v = complex(*map(int, v_data.split(", ")[:2]))
    return p,v

def part_1(rawdata, lo=200000000000000, hi=400000000000000):
    r"""
    >>> part_1('''\
    ... 19, 13, 30 @ -2,  1, -2
    ... 18, 19, 22 @ -1, -1, -2
    ... 20, 25, 34 @ -2, -2, -4
    ... 12, 31, 28 @ -1, -2, -1
    ... 20, 19, 15 @  1, -5, -3
    ... ''', 7, 27)
    2
    """
    data = [parse(line) for line in rawdata.splitlines()]
    return sum(intersect_in_square(*stone0, *stone1, lo, hi) for stone0, stone1 in it.combinations(data, r=2))

import sympy
from typing import NamedTuple

class Vector3D(NamedTuple):
    @classmethod
    def parse(cls, data):
        return cls(*map(int, data.split(",")))

    x: int
    y: int
    z: int

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... 19, 13, 30 @ -2,  1, -2
    ... 18, 19, 22 @ -1, -1, -2
    ... 20, 25, 34 @ -2, -2, -4
    ... 12, 31, 28 @ -1, -2, -1
    ... 20, 19, 15 @  1, -5, -3
    ... ''')
    47
    """
    # Adapated from https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2023/Dazbo's_Advent_of_Code_2023.ipynb
    xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")

    def hail_equations(hailstone_data:str):
        position_data, velocity_data = hailstone_data.split(" @ ")
        p = Vector3D.parse(position_data)
        v = Vector3D.parse(velocity_data)

        return [sympy.Eq((xr-p.x)*(v.y-vyr), (yr-p.y)*(v.x - vxr)), sympy.Eq((yr-p.y)*(v.z-vzr), (zr-p.z)*(v.y-vyr))]

    solution = sympy.solve(it.chain.from_iterable(hail_equations(line) for line in rawdata.splitlines()))[0]
    return int(solution[xr] + solution[yr] + solution[zr])


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
