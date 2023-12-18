#!/usr/bin/env -S pdm run python
import math, cmath
import itertools as it
import networkx as nx

from collections import deque
from enum import Enum

class Direction(Enum):
    north = -1j
    south = 1j
    east = 1
    west = -1

    def __neg__(self):
        return Direction(-self.value)

    @property
    def perpendicular(self):
        if self in (Direction.north, Direction.south):
            return Direction.east, Direction.west
        else:
            return Direction.north, Direction.south

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... 2413432311323
    ... 3215453535623
    ... 3255245654254
    ... 3446585845452
    ... 4546657867536
    ... 1438598798454
    ... 4457876987766
    ... 3637877979653
    ... 4654967986887
    ... 4564679986453
    ... 1224686865563
    ... 2546548887735
    ... 4322674655533
    ... ''')
    102
    """
    points = {complex(x,y): int(c) for y, line in enumerate(rawdata.splitlines()) for x, c in enumerate(line)}
    g = nx.DiGraph()

    for point in points:
        for source_direction in Direction: 
            for dest_direction in source_direction.perpendicular:
                cumulative_loss = 0
                for amount in 1,2,3:
                    dest = point + amount*dest_direction.value
                    if dest not in points:
                        break
                    cumulative_loss += points[dest]
                    g.add_edge((point,source_direction), (dest, dest_direction),weight=cumulative_loss)

    sources = (0,Direction.south),(0,Direction.east)
    target_coords = complex(max(p.real for p in points), max(p.imag for p in points))
    targets = (target_coords,Direction.south), (target_coords,Direction.east)
    return min(nx.dijkstra_path_length(g,s,t) for s,t in it.product(sources,targets))


def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... 2413432311323
    ... 3215453535623
    ... 3255245654254
    ... 3446585845452
    ... 4546657867536
    ... 1438598798454
    ... 4457876987766
    ... 3637877979653
    ... 4654967986887
    ... 4564679986453
    ... 1224686865563
    ... 2546548887735
    ... 4322674655533
    ... ''')
    94

    >>> part_2('''\
    ... 111111111111
    ... 999999999991
    ... 999999999991
    ... 999999999991
    ... 999999999991
    ... ''')
    71
    """
    points = {complex(x,y): int(c) for y, line in enumerate(rawdata.splitlines()) for x, c in enumerate(line)}
    g = nx.DiGraph()

    for point in points:
        for source_direction in Direction: 
            for dest_direction in source_direction.perpendicular:
                cumulative_loss = 0
                for amount in range(1, 11):
                    dest = point + amount*dest_direction.value
                    if dest not in points:
                        break

                    cumulative_loss += points[dest]
                    if amount >= 4:
                        g.add_edge((point,source_direction), (dest, dest_direction),weight=cumulative_loss)

    sources = (0,Direction.south),(0,Direction.east)
    target_coords = complex(max(p.real for p in points), max(p.imag for p in points))
    targets = (target_coords,Direction.south), (target_coords,Direction.east)
    return min(nx.dijkstra_path_length(g,s,t) for s,t in it.product(sources,targets))

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
