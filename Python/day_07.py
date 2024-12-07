import operator
from typing import List

from aoc import get_lines, extract_all_ints


def parse_input(lines):
    return [extract_all_ints(line) for line in lines]


def concat(a: str, b: str) -> int:
    return int(str(a) + str(b))


def can_be_solved(cur: int, rest: List[str], target: int, ops) -> bool:
    if not rest:
        return cur == target
    next = rest.pop(0)
    for op in ops:
        res = can_be_solved(op(cur, next), rest, target,ops)
        if res:
            return True
    rest.insert(0,next)
    return False


def part_1(lines):
    return sum(map(lambda x: x[0], filter(lambda line: can_be_solved(line[1], line[2:], line[0],[operator.add, operator.mul]), lines)))


def part_2(lines):
    return sum(map(lambda x: x[0], filter(lambda line: can_be_solved(line[1], line[2:], line[0],[operator.add, operator.mul,concat]), lines)))


def main():
    lines = get_lines("input_07.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
