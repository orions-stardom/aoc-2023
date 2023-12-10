#!/usr/bin/env -S pdm run python

import networkx as nx
import itertools as it

tiles = {
    "|": dict(north=True , south=True , east=False, west=False),
    "-": dict(north=False, south=False, east=True , west=True ),
    "L": dict(north=True , south=False, east=True , west=False),
    "J": dict(north=True , south=False, east=False, west=True ),
    "7": dict(north=False, south=True , east=False, west=True ),
    "F": dict(north=False, south=True , east=True , west=False),
    ".": dict(north=False, south=False, east=False, west=False),
    "S": dict(north=True , south=True , east=True , west=True )
}

def parse_map(rawdata: str):
    data = rawdata.splitlines()
    rows, columns = len(data), len(data[0])
    
    g = nx.Graph(rows=rows,columns=columns)

    for x,y in it.product(range(columns),range(rows)):
        symbol = data[y][x]
        g.add_node((x,y), symbol=symbol, **tiles[symbol])
        if data[y][x] == "S":
            g.graph["start"] = (x,y)

    for x,y in it.product(range(columns), range(rows)):
        here,north,south,east,west = (x,y),(x,y-1),(x,y+1),(x+1,y),(x-1,y)
        if north in g.nodes and g.nodes[here]["north"] and g.nodes[north]["south"]:
            g.add_edge(here, north)
        if south in g.nodes and g.nodes[here]["south"] and g.nodes[south]["north"]:
            g.add_edge(here, south)
        if east in g.nodes and g.nodes[here]["east"] and g.nodes[east]["west"]:
            g.add_edge(here,east)
        if west in g.nodes and g.nodes[here]["west"] and g.nodes[west]["east"]:
            g.add_edge(here,west)
        
    return g

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... .....
    ... .S-7.
    ... .|.|.
    ... .L-J.
    ... .....
    ... ''')
    4

    >>> part_1('''\
    ... ..F7.
    ... .FJ|.
    ... SJ.L7
    ... |F--J
    ... LJ...
    ... ''')
    8
    """
    g = parse_map(rawdata)
    return len(nx.find_cycle(g,source=g.graph["start"]))//2


def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... .....
    ... .S-7.
    ... .|.|.
    ... .L-J.
    ... .....
    ... ''')
    1
    
    >>> part_2('''\
    ... ...........
    ... .S-------7.
    ... .|F-----7|.
    ... .||.....||.
    ... .||.....||.
    ... .|L-7.F-J|.
    ... .|..|.|..|.
    ... .L--J.L--J.
    ... ...........
    ... ''')
    4

    >>> part_2('''\
    ... .F----7F7F7F7F-7....
    ... .|F--7||||||||FJ....
    ... .||.FJ||||||||L7....
    ... FJL7L7LJLJ||LJ.L-7..
    ... L--J.L7...LJS7F-7L7.
    ... ....F-J..F7FJ|L7L7L7
    ... ....L7.F7||L7|.L7L7|
    ... .....|FJLJ|FJ|F7|.LJ
    ... ....FJL-7.||.||||...
    ... ....L---J.LJ.LJLJ...
    ... ''')
    8

    >>> part_2('''\
    ... FF7FSF7F7F7F7F7F---7
    ... L|LJ||||||||||||F--J
    ... FL-7LJLJ||||||LJL-77
    ... F--JF--7||LJLJ7F7FJ-
    ... L---JF-JLJ.||-FJLJJ7
    ... |F|F-JF---7F7-L7L|7|
    ... |FFJF7L7F-JF7|JL---7
    ... 7-L-JL7||F7|L7F-7F7|
    ... L.L7LFJ|||||FJL7||LJ
    ... L7JLJL-JLJLJL--JLJ.L
    ... ''')
    10
    """
    g = parse_map(rawdata)
    loop = set(it.chain.from_iterable(nx.find_cycle(g,source=g.graph["start"])))

    maybe_inside = set()

    # scan first for cells that are inside the loop in one direction,
    # then eliminate any that are outside it in the other direction
    for x in range(g.graph["columns"]):
        inside = False
        on_loop_segment = False
        for y in range(g.graph["rows"]):
            if (x,y) in loop:
                if g.nodes[(x,y)]["symbol"] == "|":
                    on_loop_segment = True
                elif not on_loop_segment:
                    inside = not inside
                continue

            on_loop_segment = False

            if inside:
                maybe_inside.add((x,y))

    for y in range(g.graph["rows"]):
        inside = False
        on_loop_segment = False
        for x in range(g.graph["columns"]):
            if (x,y) in loop:
                if g.nodes[(x,y)]["symbol"] == "-":
                    on_loop_segment = True
                elif not on_loop_segment:
                    inside = not inside
                continue

            on_loop_segment = False

            if not inside:
                maybe_inside.discard((x,y))

    for y in range(g.graph["rows"]):
        print("".join(g.nodes[(x,y)]["symbol"] if (x,y) in loop else "I" if (x,y) in maybe_inside else "O" for x in range(g.graph["columns"]) ))

    return len(maybe_inside)

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
