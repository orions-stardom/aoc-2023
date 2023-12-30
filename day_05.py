#!/usr/bin/env -S pdm run python

from dataclasses import dataclass
from functools import singledispatchmethod
from parse import parse

import itertools as it
import portion as P

def interval_range(start:int, size:int) -> P.Interval:
    return P.closedopen(start, start+size)

@dataclass
class ResourceMap:
    from_resource: str
    to_resource: str
    rules: P.IntervalDict[P.Interval,int]

    def __init__(self, data:str):
        header, *rulesdata = data.splitlines()
        self.from_resource, self.to_resource = parse("{}-to-{} map:", header)
        self.rules = P.IntervalDict()
        for rule in rulesdata:
            dest_start, source_start, size = map(int, rule.split())
            def mapper(source_start, dest_start):
                def remap(x):
                    return dest_start + x - source_start
                return remap
            self.rules[interval_range(source_start, size)] = mapper(source_start, dest_start)

    @singledispatchmethod
    def __getitem__(self, source:int) -> int:
        for source_range, remap in self.rules.items():
            if source in source_range:
                return remap(source)
        return source

    @__getitem__.register
    def _(self, source:P.Interval) -> P.Interval:
        mapped, remainder = P.empty(), source
        for source_interval, remap in self.rules[source].items():
            for atomic in source_interval:
                mapped |= P.closedopen(remap(atomic.lower), remap(atomic.upper))
            remainder -= source_interval
        return mapped|remainder

@dataclass
class Almanac:
    maps: list[ResourceMap]

    def __init__(self, data:list[str]):
        self.maps = [ResourceMap(d) for d in data]

    def __getitem__(self, seed:int|P.Interval):
        resource = seed
        for transform in self.maps:
            resource = transform[resource]

        return resource

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... seeds: 79 14 55 13
    ... 
    ... seed-to-soil map:
    ... 50 98 2
    ... 52 50 48
    ... 
    ... soil-to-fertilizer map:
    ... 0 15 37
    ... 37 52 2
    ... 39 0 15
    ... 
    ... fertilizer-to-water map:
    ... 49 53 8
    ... 0 11 42
    ... 42 0 7
    ... 57 7 4
    ... 
    ... water-to-light map:
    ... 88 18 7
    ... 18 25 70
    ... 
    ... light-to-temperature map:
    ... 45 77 23
    ... 81 45 19
    ... 68 64 13
    ... 
    ... temperature-to-humidity map:
    ... 0 69 1
    ... 1 0 69
    ... 
    ... humidity-to-location map:
    ... 60 56 37
    ... 56 93 4
    ... ''')
    35
    """
    seeds_data, *rules_data = rawdata.split("\n\n")
    seeds = [int(seed) for seed in seeds_data.removeprefix("seeds:").split()]
    almanac = Almanac(rules_data)
    return min(almanac[seed] for seed in seeds)


def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... seeds: 79 14 55 13
    ... 
    ... seed-to-soil map:
    ... 50 98 2
    ... 52 50 48
    ... 
    ... soil-to-fertilizer map:
    ... 0 15 37
    ... 37 52 2
    ... 39 0 15
    ... 
    ... fertilizer-to-water map:
    ... 49 53 8
    ... 0 11 42
    ... 42 0 7
    ... 57 7 4
    ... 
    ... water-to-light map:
    ... 88 18 7
    ... 18 25 70
    ... 
    ... light-to-temperature map:
    ... 45 77 23
    ... 81 45 19
    ... 68 64 13
    ... 
    ... temperature-to-humidity map:
    ... 0 69 1
    ... 1 0 69
    ... 
    ... humidity-to-location map:
    ... 60 56 37
    ... 56 93 4
    ... ''')
    46
    """
    seeds_data, *rules_data = rawdata.split("\n\n")
    seeds = P.empty()
    for seed, size in it.batched(map(int, seeds_data.removeprefix("seeds:").split()), 2):
        seeds |= interval_range(seed, size)

    almanac = Almanac(rules_data)
    return almanac[seeds].lower

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
