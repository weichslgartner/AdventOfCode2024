import re
from functools import reduce
from typing import List, NamedTuple

from aoc import input_as_str


class Instruction(NamedTuple):
    do: str
    dont: str
    mul: str
    f_n: int
    s_n: int


def parse_input(line: str) -> List[Instruction]:
    return list(map(lambda x: Instruction(*x[:3], f_n=int(x[-2]), s_n=int(x[-1])) if x[-1] else Instruction(*x),
                    re.findall(r'(do\(\))|(don\'t\(\))|(mul\((\d{1,3}),(\d{1,3})\))', line)))


def part_1(instructions: List[Instruction]) -> int:
    return sum(map(lambda i: i.f_n * i.s_n, filter(lambda x: x.mul, instructions)))


def conditional_mul(state: (bool, int), el: Instruction) -> (bool, int):
    enabled, total = state
    if el.do:
        enabled = True
    elif el.dont:
        enabled = False
    elif el.mul and enabled:
        total += el.f_n * el.s_n
    return enabled, total


def part_2(instructions: List[Instruction]) -> int:
    return reduce(conditional_mul, instructions, (True, 0))[1]


def main():
    lines = input_as_str("input_03.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
