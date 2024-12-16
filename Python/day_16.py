import collections
from dataclasses import dataclass
import sys
import heapq
from itertools import count

from aoc import *


class Element(namedtuple('Element', 'cost, direc, point')):
    def __repr__(self):
        return f'Point({self.point}): {self.direc} {self.cost}'


def parse_input(lines):
    walls = set()
    start, end = None, None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            p = Point(x, y)
            if c == "#":
                walls.add(p)
            elif c == 'S':
                start = p
            elif c == 'E':
                end = p
    return walls, start, end


def part_1(walls, start, end):
    queue = []
    heapq.heappush(queue, (0,Direction.EAST.value, (start, Direction.EAST)))

    costs_dict = collections.defaultdict(lambda: sys.maxsize)
    while len(queue) > 0:
        cost,_, (point, direc) = heapq.heappop(queue)
        #print(cost, (point, direc) )
        if cost >= costs_dict[(point,direc)]:
            continue
        costs_dict[point,direc] = cost
        if point == end:
            continue
        p_delta = dir_to_point(direc)
        next_p = Point(x=point.x + p_delta.x, y=point.y + p_delta.y)
        if next_p not in walls:
            heapq.heappush(queue, (cost + 1,direc.value, (next_p, direc)))
        # Direction()

        for d in [Direction((direc.value + 1) % (len(Direction))),
                  Direction((direc.value - 1) % (len(Direction)))]:
            p_delta = dir_to_point(d)
            next_p = Point(x=point.x + p_delta.x, y=point.y + p_delta.y)
            if next_p not in walls:
                heapq.heappush(queue, (cost +1000 + 1, d.value, (next_p, d)))

    return min(costs_dict[(end,d)] for d in Direction)


def part_2(walls, start, end):
    pass


def main():
    lines = get_lines("input_16.txt")
    walls, start, end = parse_input(lines)
    print("Part 1:", part_1(walls, start, end))
    print("Part 2:", part_2(walls, start, end))


if __name__ == '__main__':
    main()
