#!/usr/bin/env -S pdm run python

def part_1(rawdata):
    r"""
    >>> part_1('''\
    ... 1abc2
    ... pqr3stu8vwx
    ... a1b2c3d4e5f
    ... treb7uchet''')
    142
    """
    data = rawdata.splitlines()
    def calib(line):
        digits = [d for d in line if d.isdigit()]
        return int(digits[0]+digits[-1])

    return sum(calib(line) for line in data)


def part_2(rawdata):
    r"""
    >>> part_2('''\
    ... two1nine
    ... eightwothree
    ... abcone2threexyz
    ... xtwone3four
    ... 4nineeightseven2
    ... zoneight234
    ... 7pqrstsixteen''')
    281
    """
    data = rawdata.splitlines()
    def calib(line):
        # we need to consider words instead of just numbers.. fine
        # but they can overlap :( thats a bit evil for day 1...
        real_line = line.replace("one", "one1one") \
                   .replace("two", "two2two") \
                   .replace("three", "three3three") \
                   .replace("four",  "four4four") \
                   .replace("five", "five5five") \
                   .replace("six", "six6six") \
                   .replace("seven", "seven7seven") \
                   .replace("eight", "eight8eight") \
                   .replace("nine", "nine9nine")
        digits = [d for d in real_line if d.isdigit()]
        return int(digits[0]+digits[-1])

    return sum(calib(line) for line in data)

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
