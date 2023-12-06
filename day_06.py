#!/usr/bin/env -S pdm run python

from dataclasses import dataclass
from math import sqrt, prod

import more_itertools as mit
import portion as P

@dataclass
class BoatRace:
    allowed_time: int
    best_distance: int

    @property
    def n_better_times(self):
        # The distance travelled when we hold the button for x units of time
        # is x(allowed_time - x). So we're looking for 
        #     x(allowed_time - x) > best_distance
        #     -x**2 - allowed_time*x - best_distance > 0
        # This is always an upside-down parabola, so it will be greater than 0
        # between the two roots, meaning the ways we can do better are the integers
        # in that interval

        t,d = self.allowed_time, self.best_distance

        lo, hi = (t - sqrt(t**2 - 4*d))/2, \
                 (t + sqrt(t**2 - 4*d))/2 

        positive_vals = P.open(lo,hi)
        return mit.ilen(P.iterate(positive_vals,step=1, base=int))

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... Time:      7  15   30
    ... Distance:  9  40  200
    ... ''')
    288
    """
    times_data, distances_data = rawdata.splitlines()
    times = map(int, times_data.removeprefix("Time:").split())
    distances = map(int, distances_data.removeprefix("Distance:").split())
    races = [BoatRace(time,distance) for time,distance in zip(times,distances)]
    return prod(r.n_better_times for r in races)


def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... Time:      7  15   30
    ... Distance:  9  40  200
    ... ''')
    71503
    """
    time_data, distance_data = rawdata.splitlines()
    race = BoatRace(int("".join(time_data.removeprefix("Time:").split())), 
                    int("".join(distance_data.removeprefix("Distance:").split())))
    return race.n_better_times

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
