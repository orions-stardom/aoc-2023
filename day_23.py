#!/usr/bin/env -S pdm run python
import networkx as nx
import more_itertools as mit
from collections import deque

def parse(rawdata, icy_slopes=True) -> nx.Graph:
    g = nx.DiGraph() if icy_slopes else nx.Graph()
    g.add_nodes_from((complex(x,y), dict(terrain=c)) for (y, line) in enumerate(rawdata.splitlines()) for (x, c) in enumerate(line) if c != "#")

    directions = {
        ".": [1,1j,-1,-1j],
        ">": [1],
        "<": [-1],
        "v": [1j],
        "^": [-1j],
    }

    for z in g.nodes:
        terrain = g.nodes[z]["terrain"]
        valid = directions[terrain] if icy_slopes else [1,1j,-1,-1j]
        for dz in valid:
            z1 = z+dz
            if z1 in g:
                g.add_edge(z,z1, weight=1)


    start = g.graph["start"] = mit.only(z for z in g.nodes if z.imag == 0 and g.nodes[z]["terrain"] == ".")
    max_y = max(z.imag for z in g.nodes)
    target = g.graph["target"] = mit.only(z for z in g.nodes if z.imag == max_y and g.nodes[z]["terrain"] == ".")

    # simplify the graph by collapsing all the long corridors into weighted edges between the junctions
    visited = set()
    q = deque([(start, mit.only(g[start]))])

    while q:
        here, there = q.popleft()
        visited.add(here)
        consumed = {there} 
        while len(neighbours := set(g[there]) - consumed - visited) == 1:
            there = neighbours.pop()
            consumed.add(there)

        visited.add(there)
        g.add_edge(here, there, weight=len(consumed))
        g.remove_nodes_from(consumed - visited)
        q.extend((there,n) for n in g[there] if n not in visited)

    return g

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... #.#####################
    ... #.......#########...###
    ... #######.#########.#.###
    ... ###.....#.>.>.###.#.###
    ... ###v#####.#v#.###.#.###
    ... ###.>...#.#.#.....#...#
    ... ###v###.#.#.#########.#
    ... ###...#.#.#.......#...#
    ... #####.#.#.#######.#.###
    ... #.....#.#.#.......#...#
    ... #.#####.#.#.#########v#
    ... #.#...#...#...###...>.#
    ... #.#.#v#######v###.###v#
    ... #...#.>.#...>.>.#.###.#
    ... #####v#.#.###v#.#.###.#
    ... #.....#...#...#.#.#...#
    ... #.#########.###.#.#.###
    ... #...###...#...#...#.###
    ... ###.###.#.###v#####v###
    ... #...#...#.#.>.>.#.>.###
    ... #.###.###.#.###.#.#v###
    ... #.....###...###...#...#
    ... #####################.#
    ... ''')
    94
    """
    g = parse(rawdata)
    return max(nx.path_weight(g, p, "weight") for p in nx.all_simple_paths(g, g.graph["start"], g.graph["target"]))

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... #.#####################
    ... #.......#########...###
    ... #######.#########.#.###
    ... ###.....#.>.>.###.#.###
    ... ###v#####.#v#.###.#.###
    ... ###.>...#.#.#.....#...#
    ... ###v###.#.#.#########.#
    ... ###...#.#.#.......#...#
    ... #####.#.#.#######.#.###
    ... #.....#.#.#.......#...#
    ... #.#####.#.#.#########v#
    ... #.#...#...#...###...>.#
    ... #.#.#v#######v###.###v#
    ... #...#.>.#...>.>.#.###.#
    ... #####v#.#.###v#.#.###.#
    ... #.....#...#...#.#.#...#
    ... #.#########.###.#.#.###
    ... #...###...#...#...#.###
    ... ###.###.#.###v#####v###
    ... #...#...#.#.>.>.#.>.###
    ... #.###.###.#.###.#.#v###
    ... #.....###...###...#...#
    ... #####################.#
    ... ''')
    154
    """
    g = parse(rawdata, icy_slopes=False)
    return max(nx.path_weight(g, p, "weight") for p in nx.all_simple_paths(g, g.graph["start"], g.graph["target"]))

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
