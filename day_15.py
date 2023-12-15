#!/usr/bin/env -S pdm run python

def hash(ascii_string: str):
    """
    >>> hash("HASH")
    52
    """
    value = 0
    for c in ascii_string:
        value += ord(c)
        value = value * 17 % 256
    return value

def part_1(rawdata):
    r"""
    >>> part_1('''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7''')
    1320
    """
    return sum(hash(instruction) for instruction in rawdata.split(","))

def part_2(rawdata):
    r"""
    >>> part_2('''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7''')
    145
    """
    boxes = [{} for _ in range(256)]
    for instruction in rawdata.split(","):
        if instruction.endswith("-"):
            label = instruction.removesuffix("-")
            boxes[hash(label)].pop(label, None)
        elif "=" in instruction:
            label, f = instruction.split("=")
            boxes[hash(label)][label] = int(f)
        else:
            breakpoint()

    return sum(boxnum * slot * lens for boxnum, box in enumerate(boxes, start=1)
                                    for slot, lens in enumerate(box.values(), start=1))

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
