from aoc import get_lines, line_to_int


def parse_input(lines):
    return [line_to_int(l, split_char=" ") for l in lines]


def safe(diffs):
    all_positive = all(map(lambda x: x > 0, diffs))
    all_negative = all(map(lambda x: x < 0, diffs))
    in_range = all(map(lambda x: 0 < abs(x) <= 3, diffs))
    return in_range and (all_negative or all_positive)


def part_1(levels):
    sum = 0
    for l in levels:
        diffs = [i - j for i, j in zip(l[1:], l)]
        sum += safe(diffs)
    return sum


def remove_one(levels):
    for i in range(len(levels) - 1):
        yield levels[:i] + levels[i + 1:]


def part_2(levels):
    sum = 0
    for l in levels:
        diffs = [i - j for i, j in zip(l[1:], l)]
        if safe(diffs):
            sum += 1
        else:
            for i in range(len(l)):
                l_new = l[:i] + l[i + 1:]
                diffs = [i - j for i, j in zip(l_new[1:], l_new)]
                if safe(diffs):
                    sum += 1
                    break
    return sum


def main():
    lines = get_lines("input_02.txt")
    levels = parse_input(lines)
    print("Part 1:", part_1(levels))
    print("Part 2:", part_2(levels))


if __name__ == '__main__':
    main()
