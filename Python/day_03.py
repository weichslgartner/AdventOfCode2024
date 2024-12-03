import operator

from aoc import get_lines, input_as_str, extract_all_ints
import re

def parse_input(line):
    res = re.findall(r'(?P<do>do\(\))|(?P<dont>don\'t\(\))|(?P<mul>mul\((\d+),(\d+)\))',line)
    return res


def part_1(tups):
    return sum(map(lambda x: int(x[-1])*int(x[-2]),filter(lambda x: len(x[3])>0,tups)))


def part_2(tups):
    enabled = True
    sum = 0
    for r in tups:
        if r[0] == "do()":
            enabled = True
        elif r[1] == "don't()":
            enabled = False
        elif r[2].startswith("mul"):
            if enabled:
                sum += int(r[-1])*int(r[-2])
    return sum

def main():
    test = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    lines = input_as_str("input_03.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
