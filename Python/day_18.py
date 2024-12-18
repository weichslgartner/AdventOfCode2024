import collections
import heapq
import sys
from typing import Optional

from aoc import *


def parse_input(lines: List[str]) -> List[Point]:
    return [Point(*extract_all_ints(line)) for line in lines]


def part_1(points: List[Point], target: Point = Point(70, 70), n_nbytes: int = 1024) -> int:
    return find_min_path(n_nbytes, points, target)


def find_min_path(n_nbytes: int, points: List[Point], target: Point) -> Optional[int]:
    p_max = Point(x=target.x + 1, y=target.y + 1)
    walls = {p for p in points[:n_nbytes]}
    queue = []
    heapq.heappush(queue, (0, Point(0, 0)))
    costs_dict = collections.defaultdict(lambda: sys.maxsize)
    while len(queue) > 0:
        cost, point = heapq.heappop(queue)
        if cost >= costs_dict[point]:
            continue
        costs_dict[point] = cost
        if point == target:
            return cost
        for n in filter(lambda x: x not in walls, get_neighbours_4(point, p_max)):
            heapq.heappush(queue, (cost + 1, n))
    return None


def binary_search(left: int, right: int, points: List[Point], target: Point) -> (Optional[int], Optional[int]):
    m, res = None, None
    while left <= right:
        m = (left + right) // 2
        res = find_min_path(m, points, target)
        if res is not None:
            left = m + 1
        else:
            right = m - 1
    return m, res


def part_2(points: List[Point], target: Point = Point(70, 70), start_byte: int = 1024) -> str:
    i, res = binary_search(left=start_byte, right=len(points), points=points, target=target)
    return f"{points[i - 1].x},{points[i - 1].y}" if res is None else f"{points[i].x},{points[i].y}"


def main():
    lines = get_lines("input_18.txt")
    points = parse_input(lines)
    print("Part 1:", part_1(points))
    print("Part 2:", part_2(points))


if __name__ == '__main__':
    main()
