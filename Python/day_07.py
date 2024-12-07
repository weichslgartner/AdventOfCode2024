import operator
import re
from typing import List, Tuple

from aoc import get_lines, extract_all_ints


def parse_input(lines):
    return [tuple(map(int, (re.findall(r'-?\d+', line)))) for line in lines]


def concat(a: str, b: str) -> int:
    return int(str(a) + str(b))


def can_be_solved(cur: int, numbers: Tuple[int], idx: int, ops) -> bool:
    if idx == len(numbers) - 1:
        return cur == numbers[0]
    if cur > numbers[0]:
        return False
    next_el = numbers[idx + 1]
    for op in ops:
        res = can_be_solved(op(cur, next_el), numbers, idx + 1, ops)
        if res:
            return True
    return False


def part_1(lines):
    return sum(map(lambda x: x[0], filter(lambda line: can_be_solved(line[1], line, 1,
                                                                     [operator.add, operator.mul]), lines)))


def part_2(lines):
    return sum(map(lambda x: x[0], filter(lambda line: can_be_solved(line[1], line, 1,
                                                                     [operator.add, operator.mul, concat]), lines)))


def main():
    lines = get_lines("input_07.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
