#!/usr/bin/env -S pdm run python

from collections import deque
from parse import parse

import math
import re

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... px{a<2006:qkq,m>2090:A,rfg}
    ... pv{a>1716:R,A}
    ... lnx{m>1548:A,A}
    ... rfg{s<537:gd,x>2440:R,A}
    ... qs{s>3448:A,lnx}
    ... qkq{x<1416:A,crn}
    ... crn{x>2662:A,R}
    ... in{s<1351:px,qqz}
    ... qqz{s>2770:qs,m<1801:hdj,R}
    ... gd{a>3333:R,R}
    ... hdj{m>838:A,pv}
    ... 
    ... {x=787,m=2655,a=1222,s=2876}
    ... {x=1679,m=44,a=2067,s=496}
    ... {x=2036,m=264,a=79,s=2244}
    ... {x=2461,m=1339,a=466,s=291}
    ... {x=2127,m=1623,a=2188,s=1013}
    ... ''')
    19114
    """
    workflow_data, parts_data = rawdata.split("\n\n")
    workflows = {name: body.split(",") for name,body in map(lambda line: parse("{}{{{}}}", line), workflow_data.splitlines())}

    accepted_rating = 0
    for part in parts_data.splitlines():
        x,m,a,s = parse("{{x={:d},m={:d},a={:d},s={:d}}}", part)
        workflow = "in"
        while True:
            if workflow == "R":
                break
            if workflow == "A":
                accepted_rating += x+m+a+s
                break

            for rule in workflows[workflow]:
                if ":" not in rule:
                    workflow = rule
                    break

                test, target = rule.split(":")
                category, op, threshold = parse("{}{}{:d}", test)
                if op == "<" and locals()[category] < threshold or op == ">" and locals()[category] > threshold:
                    workflow = target
                    break

    return accepted_rating

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... px{a<2006:qkq,m>2090:A,rfg}
    ... pv{a>1716:R,A}
    ... lnx{m>1548:A,A}
    ... rfg{s<537:gd,x>2440:R,A}
    ... qs{s>3448:A,lnx}
    ... qkq{x<1416:A,crn}
    ... crn{x>2662:A,R}
    ... in{s<1351:px,qqz}
    ... qqz{s>2770:qs,m<1801:hdj,R}
    ... gd{a>3333:R,R}
    ... hdj{m>838:A,pv}
    ... 
    ... {x=787,m=2655,a=1222,s=2876}
    ... {x=1679,m=44,a=2067,s=496}
    ... {x=2036,m=264,a=79,s=2244}
    ... {x=2461,m=1339,a=466,s=291}
    ... {x=2127,m=1623,a=2188,s=1013}
    ... ''')
    167409079868000
    """
    workflow_data, _ = rawdata.split("\n\n")
    workflows = {name: body.split(",") for name,body in map(lambda line: parse("{}{{{}}}", line), workflow_data.splitlines())}

    accepted_combinations = 0
    all_parts = dict.fromkeys("xmas", range(1,4001))

    q = deque([(all_parts, "in")])
    while q:
        parts, workflow = q.popleft()
        while True:
            if workflow == "R":
                break
            if workflow == "A":
                accepted_combinations += math.prod(map(len, parts.values()))
                break

            if not all(parts.values()):
                break

            for rule in workflows[workflow]:
                if ":" not in rule:
                    workflow = rule
                    break

                test, target = rule.split(":")
                category, op, threshold = parse("{}{}{:d}", test)
                if threshold in parts[category]:
                    new_parts = parts.copy()
                    start,stop = parts[category].start, parts[category].stop
                    if op == "<":
                        new_parts[category] = range(start, threshold)
                        parts[category] = range(threshold, stop)
                    else:
                        new_parts[category] = range(threshold+1, stop)
                        parts[category] = range(start,threshold+1)
                    q.append((new_parts,target))

    return accepted_combinations

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
