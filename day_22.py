#!/usr/bin/env -S pdm run python
from collections import deque
from dataclasses import dataclass
import networkx as nx

@dataclass(unsafe_hash=True)
class Brick:
    z_low: int
    z_height: int
    xy: frozenset[complex]

    def __init__(self, data:str):
        start, end = [tuple(int(c) for c in p.split(",")) for p in data.split("~")]

        match [s == e for s,e in zip(start,end)]:
            case False, True, True:
                x1, x2 = min(start[0],end[0]), max(start[0],end[0])
                self.xy = frozenset(complex(x,start[1]) for x in range(x1,x2+1))
                self.z_low = start[2]
                self.z_height = 1
            case True, False, True:
                y1, y2 = min(start[1],end[1]), max(start[1],end[1])
                self.xy = frozenset(complex(start[0],y) for y in range(y1,y2+1))
                self.z_low = start[2]
                self.z_height = 1
            case True, True, False:
                self.xy = frozenset({complex(start[0],start[1])})
                self.z_low = min(start[2],end[2])
                self.z_height = max(start[2],end[2]) - self.z_low + 1
            case True, True, True:
                self.xy = frozenset({complex(start[0],start[1])})
                self.z_low = start[2]
                self.z_height = 1
            case _:
                breakpoint()

def settle(bricks: list[Brick]):
    height_map = {}
    settled = nx.DiGraph()

    for brick in sorted(bricks, key=lambda b: b.z_low):
        height_below = max(height_map.get(p, 0) for p in brick.xy)
        final_height = height_below + brick.z_height
        for p in brick.xy:
            height_map[p] = final_height

        settled.add_node(brick, height=final_height)
        settled.add_edges_from((brick,other) for other in settled if brick.xy&other.xy and settled.nodes[other]["height"] == height_below)
    return settled

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... 1,0,1~1,2,1
    ... 0,0,2~2,0,2
    ... 0,2,3~2,2,3
    ... 0,0,4~0,2,4
    ... 2,0,5~2,2,5
    ... 0,1,6~2,1,6
    ... 1,1,8~1,1,9
    ... ''')
    5
    """
    bricks = [Brick(line) for line in rawdata.splitlines()]
    settled = settle(bricks)
    return sum(all(len(settled[other]) > 1 for other,_ in settled.in_edges(brick)) for brick in bricks)

def chain_reaction(graph, destroy) -> int:
    """
    One brick to start the trouble
    One push to seal its fate
    One filter needs some action
    One link in a chain reaction

    """
    fallen = set()
    to_fall = deque([destroy])

    while to_fall:
        falling = to_fall.popleft()
        fallen.add(falling)
        to_fall.extend(brick for brick,_ in graph.in_edges(falling) if brick not in fallen and all(other in fallen for other in graph[brick]))

    fallen.discard(destroy)
    return len(fallen)

def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... 1,0,1~1,2,1
    ... 0,0,2~2,0,2
    ... 0,2,3~2,2,3
    ... 0,0,4~0,2,4
    ... 2,0,5~2,2,5
    ... 0,1,6~2,1,6
    ... 1,1,8~1,1,9
    ... ''')
    7
    """
    bricks = [Brick(line) for line in rawdata.splitlines()]
    settled = settle(bricks)
    return sum(chain_reaction(settled, destroy=brick) for brick in bricks)

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
