import collections
from math import prod

from aoc import *

WIDTH = 101
HEIGHT = 103


# WIDTH = 7
# HEIGHT = 11
def parse_input(lines):
    points = []
    for line in lines:
        ps = extract_all_ints(line)
        points.append((Point(*ps[:2]), Point(*ps[2:])))
    return points


def part_1(points, steps=100):
    perform_movement(points, steps)
    return prod(calc_quads(points))


def perform_movement(points, steps):
    for i, p in enumerate(points):
        points[i] = (Point(x=(p[0].x + p[1].x * steps) % WIDTH, y=(p[0].y + p[1].y * steps) % HEIGHT), p[1])
    return points


def is_christmas_tree(points):
    cnt = collections.Counter(map(lambda p: p[0], points))
    for v in cnt.values():
        if v > 1:
            return False
    return True


def debug(i, points):
    cnt = collections.Counter(map(lambda point: point[0], points))
    for v in cnt.values():
        if v > 1:
            return False
    print(i, "=========")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            p = Point(x, y)
            if p in cnt:
                print(cnt[p], end="")
            else:
                print(".", end="")
        print()


def calc_quads(points):
    quads = [0] * 4
    for p in map(lambda x: x[0], points):
        if p.y < HEIGHT // 2:
            if p.x < WIDTH // 2:
                quads[0] += 1
            elif p.x > WIDTH // 2:
                quads[1] += 1
        elif p.y > HEIGHT // 2:
            if p.x < WIDTH // 2:
                quads[2] += 1
            elif p.x > WIDTH // 2:
                quads[3] += 1
    return quads


def part_2(points):
    for i in range(1_000_000):
        if is_christmas_tree(points):
            return i
        points = perform_movement(points, 1)


def main():
    lines = get_lines("input_14.txt")
    points = parse_input(lines)
    print("Part 1:", part_1(points.copy()))
    print("Part 2:", part_2(points))


if __name__ == '__main__':
    main()
