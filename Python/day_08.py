from collections import defaultdict
from itertools import combinations

from aoc import *


def parse_input(lines):
    antennas = defaultdict(list)
    points = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                continue
            if c != ".":
                antennas[c].append(Point(x=x, y=y))
                points[Point(x=x, y=y)] = c
    return antennas, Point(x=len(lines[0]), y=len(lines)), points


def find_antitodes(p1: Point, p2: Point):
    r1 = Point(x=p1.x + (p1.x - p2.x), y=p1.y + (p1.y - p2.y))
    r2 = Point(x=p2.x + (p2.x - p1.x), y=p2.y + (p2.y - p1.y))
    return r1, r2


def find_antitodes2(p1: Point, p2: Point, max_p):
    antitodes = {p1, p2}
    r1 = Point(x=p1.x + (p1.x - p2.x), y=p1.y + (p1.y - p2.y))
    while is_in_grid(r1, max_p):
        antitodes.add(r1)
        r1 = Point(x=r1.x + (p1.x - p2.x), y=r1.y + (p1.y - p2.y))
    r2 = Point(x=p2.x + (p2.x - p1.x), y=p2.y + (p2.y - p1.y))
    while is_in_grid(r2, max_p):
        antitodes.add(r2)
        r2 = Point(x=r2.x + (p2.x - p1.x), y=r2.y + (p2.y - p1.y))
    return antitodes


def part_1(antennas, max_p, points):
    antitodes = set()
    for freq, locs in antennas.items():
        for c in combinations(locs, r=2):
            print(c)
            p1, p2 = find_antitodes(c[0], c[1])
            if is_in_grid(p1, p_max=max_p):
                antitodes.add(p1)
            if is_in_grid(p2, p_max=max_p):
                antitodes.add(p2)
    return len(antitodes)


def debug_print(antitodes, max_p, points):
    for y in range(max_p.y):
        for x in range(max_p.x):
            p = Point(x, y)
            if p in antitodes:
                print("#", end="")
            elif p in points:
                print(points[p], end="")
            else:
                print(".", end="")
        print()


def part_2(antennas, max_p, points):
    antitodes = set()
    for freq, locs in antennas.items():
        for c in combinations(locs, r=2):
            ants = find_antitodes2(c[0], c[1], max_p)
            antitodes.update(ants)
    return len(antitodes)


def main():
    lines = get_lines("input_08.txt")
    antennas, max_p, points = parse_input(lines)
    print("Part 1:", part_1(antennas, max_p, points))
    print("Part 2:", part_2(antennas, max_p, points))


if __name__ == '__main__':
    main()
