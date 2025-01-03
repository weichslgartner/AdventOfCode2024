import collections
from functools import cache, reduce
from itertools import pairwise

from aoc import get_lines, Point

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
        return res_y + res_x + "A"
    if dst in "0A" and src in "741":
        return res_x + res_y + "A"
    if len(res_x) == 0 or len(res_y) == 0:
        return res_x + res_y + "A"
    if src in "963A" or (src in "852" and dst in "741"):
        return res_x + res_y + "A"
    return res_y + res_x + "A"


@cache
def directional_to_directional_single_step(src: str, dst: str) -> str:
    ps: Point = pad_directional[src]
    pd: Point = pad_directional[dst]
    x_d = pd.x - ps.x
    y_d = pd.y - ps.y
    res_x = "<" * abs(x_d) if x_d < 0 else ">" * x_d
    res_y = "^" * abs(y_d) if y_d < 0 else "v" * y_d
    if src == "<" and dst in "^A":
        return res_x + res_y + "A"
    if dst == "<" and src in "^A":
        return res_y + res_x + "A"
    if len(res_x) == 0 or len(res_y) == 0:
        return res_x + res_y + "A"
    if src in "A>":
        return res_x + res_y + "A"
    return res_y + res_x + "A"


def get_tuple_cnt(s):
    return reduce(lambda cnt, ab: cnt.update({ab: cnt[ab] + 1}) or cnt, pairwise(s), collections.defaultdict(int))


@cache
def shortest(a, b, r):
    stack = numeric_to_directional_single_step(a, b)
    cnts = get_tuple_cnt(stack)
    start = stack[0]
    for i in range(r):
        new_cnts = collections.defaultdict(int)
        res = directional_to_directional_single_step("A", start)
        for a, b in pairwise(res):
            new_cnts[(a, b)] += 1
        start = res[0]
        for k, v in cnts.items():
            res = directional_to_directional_single_step(k[0], k[1])
            new_cnts[("A", res[0])] += v
            for a, b in pairwise(res):
                new_cnts[(a, b)] += v
        cnts = new_cnts
    return sum(v for v in new_cnts.values()) + 1


def solve(codes, r):
    return sum(int(code[:-1]) * sum(shortest(a, b, r) for a, b in pairwise("A" + code)) for code in codes)


def part_1(codes):
    return solve(codes, 2)


def part_2(codes):
    return solve(codes, 25)


def main():
    lines = get_lines("input_21.txt")
    codes = parse_input(lines)
    print("Part 1:", part_1(codes))
    print("Part 2:", part_2(codes))


if __name__ == '__main__':
    main()
