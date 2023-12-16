#!/usr/bin/env -S pdm run python
import itertools as it
from collections import deque

up    = ( 0,-1)
down  = ( 0, 1)
left  = (-1, 0)
right = ( 1, 0)

def count_energised(grid, p, d):
    height,width = len(grid), len(grid[0])
    energised = set()
    seen_beams = set()
    current_beams = deque([(p,d)])

    while current_beams:
        beam = current_beams.popleft()
        if beam in seen_beams:
            continue
        seen_beams.add(beam)

        (x,y),(dx,dy) = beam

        while 0 <= x < width and 0 <= y < height:
            energised.add((x,y))
            match grid[y][x]:
                case ".":
                    pass
                case "/":
                    dx,dy = -dy,-dx
                case "\\":
                    dx,dy = dy,dx
                case "|" if dx:
                    current_beams.append(((x,y), up))
                    current_beams.append(((x,y), down))
                    break
                case "-" if dy:
                    current_beams.append(((x,y),left))
                    current_beams.append(((x,y),right))
                    break

            x,y = x+dx,y+dy

    return len(energised)

def part_1(rawdata):
    r"""
    >>> part_1(r'''
    ... .|...\....
    ... |.-.\.....
    ... .....|-...
    ... ........|.
    ... ..........
    ... .........\
    ... ..../.\\..
    ... .-.-/..|..
    ... .|....-|.\
    ... ..//.|....
    ... ''')
    46
    """
    data = rawdata.strip().splitlines()
    return count_energised(data, (0,0), right)

def part_2(rawdata):
    r"""
    >>> part_2(r'''
    ... .|...\....
    ... |.-.\.....
    ... .....|-...
    ... ........|.
    ... ..........
    ... .........\
    ... ..../.\\..
    ... .-.-/..|..
    ... .|....-|.\
    ... ..//.|....
    ... ''')
    51
    """
    data = rawdata.strip().splitlines()
    height,width = len(data), len(data[0])
    return max(count_energised(data,p,d) for p,d in it.chain(
        (((0, y), right) for y in range(height)),
        (((width-1, y), left) for y in range(height)),
        (((x, 0), down) for x in range(width)),
        (((x, height-1), up) for x in range(width))
    ))

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
