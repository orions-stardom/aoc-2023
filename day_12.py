#!/usr/bin/env -S pdm run python
import functools

@functools.cache
def count(record:str, groups: tuple[int], current_group=0):
    if not record:
        match groups:
            case []:
                return current_group == 0
            case [group]:
                return current_group == group
            case _:
                return 0
    if not groups:
        if "#" in record:
            return 0
        return 1

    if current_group > groups[0]:
        return 0

    maybe_broken = record.count("#") + record.count("?") + current_group
    if maybe_broken < sum(groups):
        return 0

    c,record = record[0], record[1:]

    res = 0
    if c == "#" or c == "?":
        res += count(record, groups, current_group+1)
    if c == "." or c == "?":
        if current_group and groups[0] == current_group:
            res += count(record, groups[1:], 0)
        elif not current_group:
            res += count(record, groups, 0)

    return res

def parse(line:str) -> tuple[str,list[int]]:
    record, groupsdata = line.split()
    groups = tuple(int(x) for x in groupsdata.split(","))
    return record, groups

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... ???.### 1,1,3
    ... .??..??...?##. 1,1,3
    ... ?#?#?#?#?#?#?#? 1,3,1,6
    ... ????.#...#... 4,1,1
    ... ????.######..#####. 1,6,5
    ... ?###???????? 3,2,1
    ... ''')
    21

    >>> part_1("???.### 1,1,3")
    1

    >>> part_1("?###???????? 3,2,1")
    10

    """
    data = [parse(line) for line in rawdata.splitlines()]
    return sum(count(*r) for r in data)

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... ???.### 1,1,3
    ... .??..??...?##. 1,1,3
    ... ?#?#?#?#?#?#?#? 1,3,1,6
    ... ????.#...#... 4,1,1
    ... ????.######..#####. 1,6,5
    ... ?###???????? 3,2,1
    ... ''')
    525152

    >>> part_2("???.### 1,1,3")
    1

    >>> part_2("?###???????? 3,2,1")
    506250

    """
    data = [parse(line) for line in rawdata.splitlines()]
    return sum(count("?".join([r]*5), n*5) for r,n in data)

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
