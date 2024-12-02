from collections import Counter
from typing import List

from aoc import get_lines


def parse_input(lines: List[str]) -> (List[int], List[int]):
    return zip(*(map(int, line.split()) for line in lines))


def part_1(one: List[int], two: List[int]) -> int:
    return sum(abs(o - t) for o, t in zip(sorted(one), sorted(two)))


def part_2(one: List[int], two: List[int]) -> int:
    cnt = Counter(two)
    return sum(i * cnt[i] for i in one)


def main():
    lines = get_lines("input_01.txt")
    one, two = parse_input(lines)
    print("Part 1:", part_1(one, two))
    print("Part 2:", part_2(one, two))


if __name__ == '__main__':
    main()
