import heapq
from functools import reduce
from collections import defaultdict
from typing import Set, List, Dict, Tuple, Any

from aoc import get_lines, Point


def parse_input(lines: List[str]) -> Dict[str, Set[Point]]:
    regions = defaultdict(set)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            regions[c].add(Point(x, y))
    return regions


def get_neighbours_4(p: Point) -> Set[Point]:
    return {Point(p.x - 1, p.y), Point(p.x, p.y - 1), Point(p.x + 1, p.y), Point(p.x, p.y + 1)}


def partition(points: Set[Point]) -> List[Set[Point]]:
    res = []
    while len(points) > 0:
        p = points.pop()
        queue = get_neighbours_4(p) & points
        region = {p}
        while len(queue) > 0:
            region |= queue & points
            new_queue = set()
            for q in queue:
                new_queue |= (get_neighbours_4(q) & points) - region
            queue = new_queue
        points -= region
        res.append(region)
    return res


# alternative solution for part2
def cnt_corners(p: Point, points: Set[Point]) -> int:
    corners = 0
    dirs = [(Point(-1, 0), Point(0, -1), Point(-1, -1)),
            (Point(0, -1), Point(1, 0), Point(1, -1)),
            (Point(1, 0), Point(0, 1), Point(1, 1)),
            (Point(0, 1), Point(-1, 0), Point(-1, 1))]
    for d in dirs:
        p1 = Point(x=p.x + d[0].x, y=p.y + d[0].y)
        p2 = Point(x=p.x + d[1].x, y=p.y + d[1].y)
        p3 = Point(x=p.x + d[2].x, y=p.y + d[2].y)
        if not ((p1 in points) or (p2 in points)):
            corners += 1
        if p1 in points and p2 in points and p3 not in points:
            corners += 1
    return corners


def add_to_sides(new_perimeter: Set[Point], p: Point, sides: Tuple[Any, Any]):
    for n in new_perimeter:
        if n.x == p.x:
            heapq.heappush(sides[0][(n.y, p.y)], p.x)
        if n.y == p.y:
            heapq.heappush(sides[1][(n.x, p.x)], p.y)


def calc_sides(sides: Tuple[defaultdict[list], defaultdict[list]]):
    n_v = 0
    for side in sides:
        for q in side.values():
            prev = -2
            while len(q) > 0:
                s = heapq.heappop(q)
                if abs(s - prev) > 1:
                    n_v += 1
                prev = s
    return n_v


def eval_region(points: Set[Point]) -> (int, int):
    perimeter = 0
    # n_corners = 0
    sides = (defaultdict(list), defaultdict(list))
    for p in points:
        new_perimeter = get_neighbours_4(p).difference(points)
        perimeter += len(new_perimeter)
        add_to_sides(new_perimeter, p, sides)
        # n_corners += cnt_corners(p, points)
    return calc_sides(sides), perimeter


def solve(regions: Dict[str, Set[Point]]) -> (int, int):
    new_regions = reduce(lambda accu, el: accu + partition(el), regions.values(), [])
    part1 = 0
    part2 = 0
    for points in new_regions:
        n, perimeter = eval_region(points)
        part1 += len(points) * perimeter
        part2 += len(points) * n
    return part1, part2


def main():
    lines = get_lines("input_12.txt")
    regions = parse_input(lines)
    part1, part2 = solve(regions)
    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == '__main__':
    main()
