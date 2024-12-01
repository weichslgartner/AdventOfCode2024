from collections import Counter

from aoc import get_lines


def parse_input(lines):
    one = []
    two = []
    for line in lines:
        o, t = line.split()
        one.append(int(o))
        two.append(int(t))
    return one, two


def part_1(one, two):
    return sum(abs(o - t) for o, t in zip(sorted(one), sorted(two)))


def part_2(one, two):
    cnt = Counter(two)
    return sum(i * cnt[i] for i in one)


def main():
    lines = get_lines("input_01.txt")
    one, two = parse_input(lines)
    print("Part 1:", part_1(one, two))
    print("Part 2:", part_2(one, two))


if __name__ == '__main__':
    main()
