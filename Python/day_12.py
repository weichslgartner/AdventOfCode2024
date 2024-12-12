import collections
from typing import Set, List, Tuple

from aoc import get_lines, Point


def parse_input(lines):
    regions = collections.defaultdict(set)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            regions[c].add(Point(x, y))
    return regions, Point(x=len(lines[0]), y=len(lines))


def get_neighbours_4(p: Point) -> Set[Point]:
    return {Point(p.x - 1, p.y), Point(p.x, p.y - 1), Point(p.x + 1, p.y), Point(p.x, p.y + 1)}


def partition(c: str, points: Set[Point]) -> List[Tuple[str, Set[Point]]]:
    res = []
    while len(points) > 0:
        p = points.pop()
        queue = get_neighbours_4(p)
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


def part_1(regions, p_max):
    new_regions = []
    for c, points in regions.items():
        new_regions += partition(c,points)
    res = 0
    for c, points in new_regions:
        perimeter = 0
        for p in points:
            perimeter += len(get_neighbours_4(p).difference(points))
       # print(c, len(points), perimeter, len(points) * perimeter)
        res += len(points) * perimeter
    return res


def part_2(regions, p_max):
    pass


def main():
    lines = get_lines("input_12.txt")
    regions, p_max = parse_input(lines)
    print("Part 1:", part_1(regions, p_max))
    print("Part 2:", part_2(regions, p_max))


if __name__ == '__main__':
    main()
