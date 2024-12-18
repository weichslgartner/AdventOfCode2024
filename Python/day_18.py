import collections
import heapq
import sys

from aoc import *


def parse_input(lines):
    return [Point(*extract_all_ints(line)) for line in lines]


def part_1(points, target=Point(70, 70), n_nbytes=1024):
    return find_min_path(n_nbytes, points, target)


def find_min_path(n_nbyes, points, target):
    start = Point(0, 0)
    p_max = Point(x=target.x + 1, y=target.y + 1)
    walls = {p for p in points[:n_nbyes]}
    queue = []
    heapq.heappush(queue, (0, start))
    costs_dict = collections.defaultdict(lambda: sys.maxsize)
    while len(queue) > 0:
        cost, point = heapq.heappop(queue)
        if cost >= costs_dict[point]:
            continue
        if cost > costs_dict[target]:
            continue
        costs_dict[point] = cost
        if point == target:
            return cost
        for n in get_neighbours_4(point, p_max):
            if n not in walls:
                heapq.heappush(queue, (cost + 1, n))
    return None


def binary_search(l, r, points, target):
    while l <= r:
        m = (l + r) // 2
        res = find_min_path(m, points, target)
        if res is not None:
            l = m + 1
        else:
            r = m - 1
    return m


def part_2(points, target=Point(70, 70), start_byte=1024):
    i = binary_search(l=start_byte, r=len(points), points=points, target=target)
    p = points[i - 1]
    return f"{p.x},{p.y}"


def main():
    lines = get_lines("input_18.txt")
    points = parse_input(lines)
    print("Part 1:", part_1(points))
    print("Part 2:", part_2(points))


if __name__ == '__main__':
    main()
