import collections
from typing import Set, List, Tuple, Dict

from aoc import get_lines, Point


def parse_input(lines: List[str]) -> Dict[str, Set[Point]]:
    regions = collections.defaultdict(set)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            regions[c].add(Point(x, y))
    return regions


def get_neighbours_4(p: Point) -> Set[Point]:
    return {Point(p.x - 1, p.y), Point(p.x, p.y - 1), Point(p.x + 1, p.y), Point(p.x, p.y + 1)}


def partition(c: str, points: Set[Point]) -> List[Tuple[str, Set[Point]]]:
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
        res.append((c, region))
    return res


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
        if (p1 not in points) and (p2 not in points):
            corners += 1
        if p1 in points and p2 in points and p3 not in points:
            corners += 1
    return corners


def solve(regions: Dict[str, Set[Point]]) -> (int, int):
    new_regions = []
    for c, points in regions.items():
        new_regions += partition(c, points)
    part1 = 0
    part2 = 0
    for c, points in new_regions:
        perimeter = 0
        n_corners = 0
        for p in sorted(points):
            perimeter += len(get_neighbours_4(p).difference(points))
            n_corners += cnt_corners(p, points)
        n = n_corners
        part1 += len(points) * perimeter
        part2 += len(points) * n
    return part1, part2


def main():
    lines = get_lines("input_12.txt")
    regions, p_max = parse_input(lines)
    part1, part2 = solve(regions)
    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == '__main__':
    main()
