from typing import List

from aoc import get_lines, line_to_int


def parse_input(lines: List[str]) -> List[List[int]]:
    return [line_to_int(i, split_char=" ") for i in lines]


def safe(diffs: List[int]) -> bool:
    all_positive = all(map(lambda x: x > 0, diffs))
    all_negative = all(map(lambda x: x < 0, diffs))
    in_range = all(map(lambda x: 0 < abs(x) <= 3, diffs))
    return in_range and (all_negative or all_positive)


def adjacent_difference(level: List[int]) -> List[int]:
    return list(map(lambda x: x[0] - x[1], zip(level[1:], level)))


def damp(level: List[int]) -> bool:
    return any(safe(adjacent_difference(level[:i] + level[i + 1:])) for i in range(len(level)))


def part_1(levels: List[List[int]]) -> int:
    return sum(safe(adjacent_difference(i)) for i in levels)


def part_2(levels: List[List[int]]) -> int:
    return sum(safe(adjacent_difference(i)) or damp(i) for i in levels)


def main():
    lines = get_lines("input_02.txt")
    levels = parse_input(lines)
    print("Part 1:", part_1(levels))
    print("Part 2:", part_2(levels))


if __name__ == '__main__':
    main()
