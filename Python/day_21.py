from functools import cache
from typing import List

from aoc import get_lines, Point
from itertools import pairwise

pad_numeric = None
pad_directional = None


def parse_input(lines):
    global pad_numeric, pad_directional
    keypad_numeric = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [None, '0', 'A']]
    keypad_directional = [[None, '^', 'A'], ['<', 'v', '>']]
    pad_numeric = grid_to_dict(keypad_numeric)
    pad_directional = grid_to_dict(keypad_directional)
    return [line for line in lines]


def grid_to_dict(keypad_numeric):
    key_dict = {}
    for y, line in enumerate(keypad_numeric):
        for x, c in enumerate(line):
            p = Point(x, y)
            if c is not None:
                key_dict[c] = p
    return key_dict


def numeric_to_directional_single_step(src: str, dst: str) -> str:
    ps: Point = pad_numeric[src]
    pd: Point = pad_numeric[dst]
    x_d = pd.x - ps.x
    y_d = pd.y - ps.y
    res_x = "<" * abs(x_d) if x_d < 0 else ">" * x_d
    res_y = "^" * abs(y_d) if y_d < 0 else "v" * y_d
    if src in "0A" and dst in "741":
        return [res_y + res_x + "A"]
    if dst in "0A" and src in "741":
        return [res_x + res_y + "A"]
    if len(res_x) == 0 or len(res_y) == 0:
        return [res_x + res_y + "A"]
    return [res_x + res_y + "A", res_y + res_x + "A"]


def directional_to_directional_single_step(src: str, dst: str, prev: str = "") -> str:
    ps: Point = pad_directional[src]
    pd: Point = pad_directional[dst]
    x_d = pd.x - ps.x
    y_d = pd.y - ps.y
    res_x = "<" * abs(x_d) if x_d < 0 else ">" * x_d
    res_y = "^" * abs(y_d) if y_d < 0 else "v" * y_d
    if src == "<" and dst in "^A":
        return [res_x + res_y + "A"]
    if dst == "<" and src in "^A":
        return [res_y + res_x + "A"]
    if len(res_x) == 0 or len(res_y) == 0:
        return [res_x + res_y + "A"]
    return [res_x + res_y + "A", res_y + res_x + "A"]


def part_1(codes):
    complexity = 0
    for code in codes:
        tmp = 0
        for a, b in pairwise("A" + code):
            tmp += shortest(a, b)
        print(code, tmp)
        complexity += int(code[:-1]) * tmp
    return complexity


@cache
def shortest(a, b):
    stack = []
    stack += numeric_to_directional_single_step(a, b)
    for _ in range(2):
        new_stack = []
        for s in stack:
            substack = []
            for a1, b1 in pairwise("A" + s):
                substack.append(directional_to_directional_single_step(a1, b1))
            results = []
            gen_combinations("", substack, results)
            new_stack += results
        stack = new_stack
    min_val = min(len(s) for s in stack)
    return min_val


def gen_combinations(cur: str, rest: List, results: List):
    if len(rest) == 0:
        results.append(cur)
        return
    choices = rest[0]
    new_rest = rest[1:]
    for c in choices:
        gen_combinations(cur + c, new_rest, results)


def generate_shortest_num_dir(code):
    res = ""
    for a, b in pairwise("A" + code):
        res += numeric_to_directional_single_step(a, b)[0]
    print(res)
    return res


def part_2(lines):
    pass


def main():
    lines = get_lines("input_21.txt")
    codes = parse_input(lines)
    # shortest("3","7")

    print("Part 1:", part_1(codes))  # too high 157942
    print("Part 2:", part_2(codes))


if __name__ == '__main__':
    main()
