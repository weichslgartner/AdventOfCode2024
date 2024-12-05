from collections import defaultdict
from typing import List

from aoc import input_as_str, extract_all_ints


def parse_input(lines):
    rules_, pages = lines.split("\n\n", maxsplit=2)
    rules = defaultdict(set)
    [rules[x[0]].add(x[1]) for x in map(extract_all_ints, rules_.splitlines())]
    pages = [extract_all_ints(i) for i in pages.splitlines()]
    return rules, pages


def part_1(rules, pages):
    cnt = 0
    for update in pages:
        if is_in_order(update, rules):
            cnt += update[len(update) // 2]
    return cnt


def is_in_order(update, rules) -> bool:
    for i, p in reversed(list(enumerate(update))):
        rest = set(update[:i])
        if rest & rules[p]:
            return False
    return True


def fix(cur, rest, rules) -> List[int]:
    if len(rest) == 0 and is_in_order(rest, rules):
        return cur
    for i in rest:
        next_cur = cur.copy()
        next_cur.append(i)
        if is_in_order(next_cur, rules):
            next_rest = rest.copy()
            next_rest.remove(i)
            result = fix(next_cur, next_rest, rules)
            if result is not None:
                return result
    return None


def part_2(rules, pages):
    cnt = 0
    for update in pages:
        if not is_in_order(update, rules):
            update = fix([], update, rules)
            cnt += update[len(update) // 2]
    return cnt


def main():
    lines = input_as_str("input_05.txt")
    rules, pages = parse_input(lines)
    print("Part 1:", part_1(rules, pages))
    print("Part 2:", part_2(rules, pages))


if __name__ == '__main__':
    main()
