#!/usr/bin/env -S pdm run python
from __future__ import annotations

import math
import re
import itertools as it

def walk(graph, instructions, start, possible_ends):
    node = start
    for step, instruction in enumerate(it.cycle(instructions), start=1):
        node = graph[node][instruction == "R"]
        if node in possible_ends:
            return step

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... RL
    ... 
    ... AAA = (BBB, CCC)
    ... BBB = (DDD, EEE)
    ... CCC = (ZZZ, GGG)
    ... DDD = (DDD, DDD)
    ... EEE = (EEE, EEE)
    ... GGG = (GGG, GGG)
    ... ZZZ = (ZZZ, ZZZ)
    ... ''')
    2
    >>> part_1('''\
    ... LLR
    ... 
    ... AAA = (BBB, BBB)
    ... BBB = (AAA, ZZZ)
    ... ZZZ = (ZZZ, ZZZ)
    ... ''')
    6
    """
    instructions, graphdata = rawdata.split("\n\n")
    graph = {node: (left, right) for node, left, right in re.findall(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", graphdata)}
    return walk(graph, instructions, "AAA", ["ZZZ"])

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... LR
    ... 
    ... 11A = (11B, XXX)
    ... 11B = (XXX, 11Z)
    ... 11Z = (11B, XXX)
    ... 22A = (22B, XXX)
    ... 22B = (22C, 22C)
    ... 22C = (22Z, 22Z)
    ... 22Z = (22B, 22B)
    ... XXX = (XXX, XXX)
    ... ''')
    6
    """
    instructions, graphdata = rawdata.split("\n\n")
    graph = {node: (left, right) for node, left, right in re.findall(r"(\w{3}) = \((\w{3}), (\w{3})\)", graphdata)}

    startnodes = [node for node in graph if node.endswith("A")]
    endnodes = [node for node in graph if node.endswith("Z")]
    times = [walk(graph, instructions, start, endnodes) for start in startnodes]
    return math.lcm(*times)

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
