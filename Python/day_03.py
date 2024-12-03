import re
from functools import reduce

from aoc import input_as_str


def parse_input(line):
    return list(map(lambda x: (*x[0:3], int(x[-2]), int(x[-1])) if x[-1] else x,
                    re.findall(r'(do\(\))|(don\'t\(\))|(mul\((\d+),(\d+)\))', line)))


def part_1(tups):
    return sum(map(lambda x: x[-1] * x[-2], filter(lambda x: len(x[2]) > 0, tups)))


def conditional_mul(state, r):
    enabled, total = state
    if r[0] == "do()":
        enabled = True
    elif r[1] == "don't()":
        enabled = False
    elif r[2].startswith("mul"):
        total += r[-1] * r[-2] if enabled else 0
    return enabled, total


def part_2(tups):
    return reduce(conditional_mul, tups, (True, 0))[1]


def main():
    test = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    lines = input_as_str("input_03.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
