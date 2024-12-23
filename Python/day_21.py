import collections
from functools import cache
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
        return [res_y + res_x + "A"]
    if dst in "0A" and src in "741":
        return [res_x + res_y + "A"]
    if len(res_x) == 0 or len(res_y) == 0:
        return [res_x + res_y + "A"]
    if src in "963A" or (src in "852" and dst in "741"):
        return [res_x + res_y + "A"]
    return [res_y + res_x + "A"]


@cache
def directional_to_directional_single_step(src: str, dst: str) -> str:
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
    if src in "A>":
        return [res_x + res_y + "A"]
    return [res_y + res_x + "A"]


def get_tuple_cnt(s):
    cnt = collections.defaultdict(int)
    for a1, b1 in pairwise(s):
        cnt[(a1, b1)] += 1
    return cnt


@cache
def shortest(a, b, r):
    stack = []
    stack += numeric_to_directional_single_step(a, b)
    cnts = [get_tuple_cnt(s) for s in stack]
    starts = [s[0] for s in stack]
    for i in range(r):
        new_cnts = []
        new_starts = []
        for i, s in enumerate(cnts):
            new_cnt = collections.defaultdict(int)
            res = directional_to_directional_single_step("A", starts[i])[0]

            for a, b in pairwise(res):
                new_cnt[(a, b)] += 1
            new_starts.append(res[0])
            for k, v in cnts[i].items():
                res = directional_to_directional_single_step(k[0], k[1])[0]
                new_cnt[("A", res[0])] += v
                for a, b in pairwise(res):
                    new_cnt[(a, b)] += v
            new_cnts.append(new_cnt)

        cnts = new_cnts
        starts = new_starts
    return min((sum(v for v in cnt.values()) + 1) for cnt in new_cnts)


def solve(codes, r):
    complexity = 0
    for code in codes:
        tmp = 0
        for a, b in pairwise("A" + code):
            tmp += shortest(a, b, r)
        # print(code, tmp)
        complexity += int(code[:-1]) * tmp
    return complexity


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
