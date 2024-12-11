import math
from typing import List

from aoc import extract_all_ints, input_as_str
from functools import cache


def parse_input(input_str: str) -> List[int]:
    return extract_all_ints(input_str)


def transform_stone(i: int) -> List[int]:
    if i == 0:
        return [1]
    length = math.floor(math.log10(i)) + 1
    if length % 2 == 0:
        half_pow = 10 ** (length // 2)
        return [i // half_pow, i % half_pow]
    return [i * 2024]


@cache
def convert_number(num: int, n_iter: int) -> int:
    if n_iter == 0:
        return 1
    return sum(map(lambda i: convert_number(i, n_iter - 1), transform_stone(num)))


def solve(nums: List[int], n_iter: int) -> int:
    return sum(map(lambda n: convert_number(n, n_iter), nums))


def part_1(nums: List[int]) -> int:
    return solve(nums, n_iter=25)


def part_2(nums: List[int]) -> int:
    return solve(nums, n_iter=75)


def main():
    lines = input_as_str("input_11.txt")
    nums = parse_input(lines)
    print("Part 1:", part_1(nums))
    print("Part 2:", part_2(nums))


if __name__ == '__main__':
    main()
