#!/usr/bin/env -S pdm run python
import networkx as nx
import more_itertools as mit

def parse(rawdata):
    g = nx.Graph()
    for line in rawdata.splitlines():
        lhs, rhses = line.split(":")
        for rhs in rhses.split():
            g.add_edge(lhs,rhs, capacity=1)
    return g

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... jqt: rhn xhk nvd
    ... rsh: frs pzl lsr
    ... xhk: hfx
    ... cmg: qnr nvd lhk bvb
    ... rhn: xhk bvb hfx
    ... bvb: xhk hfx
    ... pzl: lsr hfx nvd
    ... qnr: nvd
    ... ntq: jqt hfx bvb xhk
    ... nvd: lhk
    ... lsr: lhk
    ... rzs: qnr cmg lsr rsh
    ... frs: qnr lhk lsr
    ... ''')
    54
    """
    g = parse(rawdata)
    start = mit.first(g)
    candidates = [n for n in g if n != start]

    for candidate in candidates:
        cuts, (partition1, partition2) = nx.minimum_cut(g, start, candidate)
        if cuts == 3:
            # blithely assume this is the only possible solution
            return len(partition1) * len(partition2)

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
