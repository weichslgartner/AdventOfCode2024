from functools import cache
from typing import Tuple, List

from aoc import input_as_str


def parse_input(input_str: str) -> (Tuple[str], List[str]):
    towels, patterns = input_str.split("\n\n", maxsplit=1)
    return tuple(t.strip() for t in towels.strip().split(",")), [p for p in patterns.splitlines()]


@cache
def cnt_valid_designs(towels: Tuple[str], pattern: str) -> int:
    if len(pattern) == 0:
        return 1
    valid_towels = filter(lambda t: pattern.startswith(t), towels)
    return sum(cnt_valid_designs(towels, pattern[len(t):]) for t in valid_towels)


def part_1(towels: Tuple[str], patterns: List[str]) -> int:
    return sum(n for n in map(lambda x: x > 0, map(lambda p: cnt_valid_designs(towels, p), patterns)))


def part_2(towels: Tuple[str], patterns: List[str]) -> int:
    return sum(cnt_valid_designs(towels, p) for p in patterns)


def main():
    input_str = input_as_str("input_19.txt")
    towels, patterns = parse_input(input_str)
    print("Part 1:", part_1(towels, patterns))
    print("Part 2:", part_2(towels, patterns))


if __name__ == '__main__':
    main()
