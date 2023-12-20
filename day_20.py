#!/usr/bin/env -S pdm run python
from __future__ import annotations
from collections import deque, defaultdict
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import math
import itertools as it
import more_itertools as mit

@dataclass
class Module(ABC):
    targets: list[str]
    inputs: dict[str, bool] = field(default_factory=dict)

    @abstractmethod
    def pulse(self, source: str, level:bool) -> bool|None:
        pass

class FlipFlop(Module):
    on: bool = False

    def pulse(self, source:str, level:bool) -> bool|None:
        if level:
            return None
        self.on = not self.on
        return self.on

class Conjunction(Module):
    def pulse(self, source:str, level: bool) -> bool:
        self.inputs[source] = level
        return not all(self.inputs.values())

class Broadcaster(Module):
    def pulse(self, source:str, level:bool) -> bool:
        return level

module_types = {"%": FlipFlop, "&": Conjunction}

def parse(rawdata:str) -> dict[str,Module]:
    modules = {}
    inputs = defaultdict(list)

    for line in rawdata.splitlines():
        name, target_list = line.split(" -> ")
        targets = target_list.split(", ")
        if name == "broadcaster":
            modules[name] = Broadcaster(targets)
        else:
            type_, name = name[0], name[1:]
            modules[name] = module_types[type_](targets)

        for target in targets: 
            inputs[target].append(name)

    for target, sources in inputs.items():
        try:
            modules[target].inputs = dict.fromkeys(sources, False)
        except KeyError:
            # the "output" module in the example doesn't ever appear as
            # an input and doesn't actually do anything
            pass
    return modules

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... broadcaster -> a, b, c
    ... %a -> b
    ... %b -> c
    ... %c -> inv
    ... &inv -> a
    ... ''')
    32000000

    >>> part_1('''\
    ... broadcaster -> a
    ... %a -> inv, con
    ... &inv -> b
    ... %b -> con
    ... &con -> output
    ... ''')
    11687500
    """
    modules = parse(rawdata)
    high_pulses = 0
    low_pulses = 0

    # now everything's set up, lets push the button
    for _ in range(1000):
        pulse_queue = deque([("button", "broadcaster", False)])
        while pulse_queue:
            source, target, level = pulse_queue.popleft()
            # print(f"{source} -{'high' if level else 'low'}-> {target}")
            if level:
                high_pulses += 1
            else:
                low_pulses += 1

            if target not in modules:
                continue

            result = modules[target].pulse(source, level)
            if result is not None:
                pulse_queue.extend((target, next_target, result) for next_target in modules[target].targets)

    return high_pulses * low_pulses

def part_2(rawdata):
    modules = parse(rawdata)
    interesting = modules[mit.only(m for m in modules if "rx" in modules[m].targets)]
    assert isinstance(interesting, Conjunction)
    interesting_counts = dict.fromkeys(interesting.inputs, None) 

    for presses in it.count(1):
        pulse_queue = deque([("button", "broadcaster", False)])
        while pulse_queue:
            source, target, level = pulse_queue.popleft()
            if target not in modules:
                continue

            result = modules[target].pulse(source, level)
            if result is not None:
                pulse_queue.extend((target, next_target, result) for next_target in modules[target].targets)

            # the only module that forwards to rx is a Conjunction, so it will
            # send low when it has most recetnly received high from all its inputs
            for m, c in interesting_counts.items():
                if interesting.inputs[m] and c is None:
                    interesting_counts[m] = presses
        
            if None not in interesting_counts.values():
                return math.lcm(*interesting_counts.values())

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
