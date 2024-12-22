from functools import reduce
from typing import List, Dict, Tuple

from aoc import get_lines

PATTERN_LENGTH = 4


def parse_input(lines: List[str]) -> List[int]:
    return [int(line) for line in lines]


def calc_secret_numbers(secret_number: int, rounds: int = 2000) -> (int, List[int]):
    prices = []
    for _ in range(rounds):
        prices.append(secret_number % 10)
        secret_number = (secret_number ^ (secret_number * 64 % 16777216))
        secret_number = (secret_number ^ (secret_number // 32))
        secret_number = (secret_number ^ (secret_number * 2048 % 16777216))
    return secret_number, prices


def calc_price_for_pattern(p: List[int]) -> Dict[Tuple, int]:
    diffs = [i - j for i, j in zip(p[1:], p)]
    pattern_dict = {}
    for i in range(len(p) - PATTERN_LENGTH):
        pattern = tuple(diffs[i:i + PATTERN_LENGTH])
        if pattern not in pattern_dict:
            pattern_dict[pattern] = p[i + PATTERN_LENGTH]
    return pattern_dict


def part_1(secrets: List[int]) -> int:
    return sum(s for s in secrets)


def part_2(prices: List[int]) -> int:
    all_sequences = reduce(
        lambda acc, p_dict: {key: acc.get(key, 0) + p_dict.get(key, 0)
                             for key in acc.keys() | p_dict.keys()},
        map(calc_price_for_pattern, prices),
        {}
    )
    return max(all_sequences.values())


def main():
    lines = get_lines("input_22.txt")
    numbers = parse_input(lines)
    secrets = [calc_secret_numbers(n) for n in numbers]
    print("Part 1:", part_1([secret for secret, _ in secrets]))
    print("Part 2:", part_2([prices for _, prices in secrets]))


if __name__ == '__main__':
    main()
