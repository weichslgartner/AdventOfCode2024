from collections import defaultdict
from itertools import combinations

from aoc import  *


def parse_input(lines ):
    antennas = defaultdict(list)
    points = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c=="#":
                continue
            if c != ".":
                antennas[c].append(Point(x=x,y=y))
                points[Point(x=x,y=y)] = c
    return antennas, Point(x=len(lines[0]), y=len(lines)),points

def find_antitodes(p1:Point,p2:Point):
    r1 = Point(x=p1.x+(p1.x-p2.x),y=p1.y+(p1.y-p2.y))
    r2 = Point(x=p2.x+(p2.x-p1.x),y=p2.y+(p2.y-p1.y))
    return r1,r2

def part_1(antennas, max_p,points):
    antitodes = set()
    print(antennas)
    for freq,locs in antennas.items():
        for c in combinations(locs,r=2):
            print(c)
            p1,p2 = find_antitodes(c[0],c[1])
            if is_in_grid(p1,p_max=max_p):
                antitodes.add(p1)
            if is_in_grid(p2,p_max=max_p):
                antitodes.add(p2)
    debug_print(antitodes, max_p, points)
    return len(antitodes)


def debug_print(antitodes, max_p, points):
    for y in range(max_p.y):
        for x in range(max_p.x):
            p = Point(x, y)
            if p in points:
                print(points[p], end="")
            if p in antitodes:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part_2(lines):
    pass


def main():
    lines = get_lines("input_08.txt")
    antennas, max_p,points = parse_input(lines)
    print("Part 1:", part_1(antennas, max_p,points))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
