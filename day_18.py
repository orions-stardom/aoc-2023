#!/usr/bin/env -S pdm run python

def trace_area(p0):
    shoelace_area = 0
    boundary_points = 0
    while True:
        try:
            distance, direction = yield
        except:
            break

        boundary_points += distance
        p1 = p0 + distance*direction
        shoelace_area += p0.real*p1.imag - p0.imag*p1.real
        p0 = p1

    area = abs(shoelace_area // 2)
    internal_points = area - boundary_points/2 + 1
    yield int(internal_points + boundary_points)


def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... R 6 (#70c710)
    ... D 5 (#0dc571)
    ... L 2 (#5713f0)
    ... D 2 (#d2c081)
    ... R 2 (#59c680)
    ... D 2 (#411b91)
    ... L 5 (#8ceee2)
    ... U 2 (#caa173)
    ... L 1 (#1b58a2)
    ... U 2 (#caa171)
    ... R 2 (#7807d2)
    ... U 3 (#a77fa3)
    ... L 2 (#015232)
    ... U 2 (#7a21e3)
    ... ''')
    62
    """
    directions = {"U": 1j, "D": -1j, "R": 1, "L":-1}

    polygon = trace_area(0)
    next(polygon)
    for line in rawdata.splitlines():
        direction, amount, _ = line.split()
        polygon.send((int(amount), directions[direction]))
    
    return polygon.send(None)

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... R 6 (#70c710)
    ... D 5 (#0dc571)
    ... L 2 (#5713f0)
    ... D 2 (#d2c081)
    ... R 2 (#59c680)
    ... D 2 (#411b91)
    ... L 5 (#8ceee2)
    ... U 2 (#caa173)
    ... L 1 (#1b58a2)
    ... U 2 (#caa171)
    ... R 2 (#7807d2)
    ... U 3 (#a77fa3)
    ... L 2 (#015232)
    ... U 2 (#7a21e3)
    ... ''')
    952408144115
    """
    directions = [1, -1j, -1, 1j]
    polygon = trace_area(0)
    next(polygon)
    for line in rawdata.splitlines():
        distance, direction = divmod(int(line.split()[2][2:-1], 16),16)
        polygon.send((distance, directions[direction]))
    
    return polygon.send(None)

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
