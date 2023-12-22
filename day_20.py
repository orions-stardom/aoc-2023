#!/usr/bin/env -S pdm run python
from collections import deque, defaultdict
import math
import itertools as it
import more_itertools as mit
import networkx as nx
import re

def parse(rawdata:str) -> nx.Graph:
    modules = nx.DiGraph() 
    inputs = defaultdict(list)
    modules.add_edge("button", "broadcaster", level=False)

    for line in rawdata.splitlines():
        source, target_list = line.split(" -> ")
        targets = target_list.split(", ")

        module_type, name = re.fullmatch("([%&]?)(.+)", source).groups()
        for target in targets:
            modules.add_edge(name, target, level=False)

        modules.nodes[name]["type"] = module_type
        
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
    pulses = {True: 0, False: 0}

    # now everything's set up, lets push the button
    for _ in range(1000):
        pulse_queue = deque([("button", "broadcaster", False)])
        while pulse_queue:
            source, target, level = pulse_queue.popleft()
            # print(f"{source} -{'high' if level else 'low'}-> {target}")
            pulses[level] += 1
            modules.edges[source, target]["level"] = level

            match modules.nodes[target].get("type"):
                case "%": # flip-flop
                    if level:
                        continue
                    modules.nodes[target]["on"] = not modules.nodes[target].get("on", False)
                    send_level = modules.nodes[target]["on"]
                case "&":  # conjunction
                    send_level = not all(modules.edges[n, target]["level"] for n, _ in modules.in_edges(target))
                case _: # broadcast
                    send_level = level

            pulse_queue.extend((target, next_target, send_level) for next_target in modules[target])

    return math.prod(pulses.values())

def part_2(rawdata):
    modules = parse(rawdata)
    interesting = mit.only(modules.in_edges("rx"))[0]
    assert modules.nodes[interesting]["type"] == "&" 
    # track the period of all the inputs to `interesting` as we see them go high
    periods = {} 

    for presses in it.count(1):
        pulse_queue = deque([("button", "broadcaster", False)])
        while pulse_queue:
            source, target, level = pulse_queue.popleft()

            if target == interesting and level:
                periods.setdefault(source, presses)
        
            if periods.keys() == {s for s,_ in modules.in_edges(interesting)}:
                return math.lcm(*periods.values())

            # print(f"{source} -{'high' if level else 'low'}-> {target}")
            modules.edges[source, target]["level"] = level
            match modules.nodes[target].get("type"):
                case "%": # flip-flop
                    if level:
                        continue
                    modules.nodes[target]["on"] = not modules.nodes[target].get("on", False)
                    send_level = modules.nodes[target]["on"]
                case "&":  # conjunction
                    send_level = not all(modules.edges[n, target]["level"] for n, _ in modules.in_edges(target))
                case _: # broadcast
                    send_level = level

            pulse_queue.extend((target, next_target, send_level) for next_target in modules[target])

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
