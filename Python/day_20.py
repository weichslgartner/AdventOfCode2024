import collections
import sys
from typing import List, Set, Iterator

from aoc import get_lines, Point, get_neighbours_4, is_in_grid


def parse_input(lines: List[str]) -> (Set[Point], Point, Point):
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

def get_neighbours_4_long(p: Point, p_max: Point) -> Iterator[Point]:
    points = [Point(p.x - 2, p.y), Point(p.x, p.y - 2), Point(p.x + 2, p.y), Point(p.x, p.y + 2)]
    return filter(lambda x: is_in_grid(x, p_max), points)

def part_1(walls: Set[Point], start: Point, end: Point):
    p_max = Point(x=max(w.x for w in walls), y=max(w.y for w in walls))

    costs_dict, path=  calc_costs(end, start, walls,p_max)
    normal_cost = costs_dict[end]
    savings = collections.defaultdict(int)
    for p in path:
        for n in get_neighbours_4_long(p,p_max):
            if n not in walls and costs_dict[n] > costs_dict[p]:
                new_costs = costs_dict[p] + 2 + (normal_cost - costs_dict[n])
                saved = normal_cost - new_costs
                if saved > 0:
                    savings[saved]+=1
                print("cheat possible",p,n, new_costs, saved )
    print(savings)
    return sum(v if k >=100 else 0 for k,v in savings.items())


def calc_costs(end, start, walls,p_max):
    stack = [(0, start)]
    costs_dict = {}
    path = [start]
    while len(stack) > 0:
        cost, point = stack.pop()
        costs_dict[point] = cost
        if point == end:
            return costs_dict, path
        for n in filter(lambda x: x not in walls and x not in costs_dict, get_neighbours_4(point, p_max)):
            stack.append((cost + 1, n))
            path.append(n)
    return costs_dict, path


def part_2(walls, start, end):
    pass


def main():
    lines = get_lines("input_20.txt")
    walls, start, end = parse_input(lines)
    print("Part 1:", part_1(walls, start, end))
    print("Part 2:", part_2(walls, start, end))


if __name__ == '__main__':
    main()
