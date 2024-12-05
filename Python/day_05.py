import functools
import heapq
from collections import defaultdict
from typing import List, Set

from aoc import input_as_str, extract_all_ints


def parse_input(input_str: str) -> (dict[int, Set[int]], List[List[int]]):
    rules_, pages = input_str.split("\n\n", maxsplit=2)
    rules = defaultdict(set)
    [rules[x[0]].add(x[1]) for x in map(extract_all_ints, rules_.splitlines())]
    return rules, [extract_all_ints(i) for i in pages.splitlines()]


def part_1(rules: dict[int, Set[int]], pages: List[List[int]]) -> int:
    cnt = 0
    for update in pages:
        if is_in_order(update, rules):
            cnt += update[len(update) // 2]
    return cnt


def is_in_order(update: List[int], rules: dict[int, Set[int]]) -> bool:
    for i, p in reversed(list(enumerate(update))):
        rest = set(update[:i])
        if rest & rules[p]:
            return False
    return True


def part_2(rules: dict[int, Set[int]], pages: List[List[int]]) -> int:
    return sum(
        map(lambda x:
            heapq.nsmallest(len(x) // 2 + 1, x, key=functools.cmp_to_key(lambda a, b: -1 if b in rules[a] else 1))[-1],
            filter(lambda x: not is_in_order(x, rules), pages)))


def main():
    lines = input_as_str("input_05.txt")
    rules, pages = parse_input(lines)
    print("Part 1:", part_1(rules, pages))
    print("Part 2:", part_2(rules, pages))


if __name__ == '__main__':
    main()
