import collections
from typing import List, Set, Dict

from aoc import get_lines, Point, get_neighbours_4, is_in_grid, manhattan_distance


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


def calc_costs(end: Point, start: Point, walls: Set[Point], p_max: Point) -> (Dict[Point, int], List[Point]):
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


def get_cheat_destinations(p: Point, p_max: Point, walls, costs_dict, save_at_least, max_dist=2) -> Set[Point]:
    point_set = set()
    for y in range(-max_dist, max_dist + 1):
        for x in range(-max_dist, max_dist + 1):
            n = Point(p.x + x, p.y + y)
            if (n not in walls and manhattan_distance(p, n) <= max_dist and is_in_grid(n, p_max) and
                    costs_dict[n] >= costs_dict[p] + manhattan_distance(p, n) + save_at_least):
                point_set.add(n)
    return point_set


def calc_savings(costs_dict: Dict[Point, int], n: Point, normal_cost: int, p: Point) -> int:
    new_costs = costs_dict[p] + manhattan_distance(p, n) + (normal_cost - costs_dict[n])
    return normal_cost - new_costs


def solve(start: Point, end: Point, walls: Set[Point], max_dist: int, save_at_least: int = 100) -> int:
    p_max = Point(x=max(w.x for w in walls), y=max(w.y for w in walls))
    costs_dict, path = calc_costs(end, start, walls, p_max)
    normal_cost = costs_dict[end]
    savings = collections.defaultdict(int)
    for p in path[:-save_at_least]:
        for n in get_cheat_destinations(p, p_max, walls, costs_dict, save_at_least=save_at_least, max_dist=max_dist):
            savings[calc_savings(costs_dict, n, normal_cost, p)] += 1
    return sum(savings.values())


def part_1(walls: Set[Point], start: Point, end: Point) -> int:
    return solve(start, end, walls, max_dist=2, save_at_least=100)


def part_2(walls: Set[Point], start: Point, end: Point) -> int:
    return solve(start, end, walls, max_dist=20, save_at_least=100)


def main():
    lines = get_lines("input_20.txt")
    walls, start, end = parse_input(lines)
    print("Part 1:", part_1(walls, start, end))
    print("Part 2:", part_2(walls, start, end))


if __name__ == '__main__':
    main()
