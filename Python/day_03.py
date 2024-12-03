import re
from functools import reduce
from typing import List, Tuple

from aoc import input_as_str


def parse_input(line: str) -> List[Tuple]:
    return list(map(lambda x: (*x[0:3], int(x[-2]), int(x[-1])) if x[-1] else x,
                    re.findall(r'(do\(\))|(don\'t\(\))|(mul\((\d+),(\d+)\))', line)))


def part_1(tups: List[tuple]) -> int:
    return sum(map(lambda x: x[-1] * x[-2], filter(lambda x: len(x[2]) > 0, tups)))


def conditional_mul(state: (bool, int), el: Tuple) -> (bool, int):
    enabled, total = state
    if el[0] == "do()":
        enabled = True
    elif el[1] == "don't()":
        enabled = False
    elif el[2].startswith("mul") and enabled:
        total += el[-1] * el[-2]
    return enabled, total


def part_2(tups: List[Tuple]) -> int:
    return reduce(conditional_mul, tups, (True, 0))[1]


def main():
    lines = input_as_str("input_03.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
