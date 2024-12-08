from collections import defaultdict
from functools import reduce
from itertools import combinations
from typing import Set, Dict, List

from aoc import Point, is_in_grid, get_lines


def parse_input(lines: List[str]) -> (Dict[str, Set[Point]], Point):
    return (reduce(lambda acc, coord: acc[coord[2]].append(Point(x=coord[1], y=coord[0])) or acc,
                   ((y, x, c)
                    for y, line in enumerate(lines)
                    for x, c in enumerate(line)
                    if c not in {".", "#"}
                    ), defaultdict(list), ), Point(x=len(lines[0]), y=len(lines)))


def find_antinodes(p1: Point, p2: Point, p_max: Point, part2: bool = False) -> Set[Point]:
    antinodes = {p1, p2} if part2 else set()
    for p_start, p_delta_x, p_delta_y in [(p1, p1.x - p2.x, p1.y - p2.y),
                                          (p2, p2.x - p1.x, p2.y - p1.y)]:
        r = Point(x=p_start.x + p_delta_x, y=p_start.y + p_delta_y)
        while is_in_grid(r, p_max):
            antinodes.add(r)
            if not part2:
                break
            r = Point(x=r.x + p_delta_x, y=r.y + p_delta_y)
    return antinodes


def solve(antennas: Dict[str, Set[Point]], max_p: Point, part2: bool) -> int:
    return len(reduce(
        lambda acc, locs: acc | reduce(
            lambda inner_acc, pair: inner_acc | find_antinodes(pair[0], pair[1], max_p, part2=part2),
            combinations(locs, r=2),
            set()
        ),
        antennas.values(),
        set()
    ))


def part_1(antennas: Dict[str, Set[Point]], p_max: Point) -> int:
    return solve(antennas, p_max, part2=False)


def part_2(antennas: Dict[str, Set[Point]], p_max: Point) -> int:
    return solve(antennas, p_max, part2=True)


def main():
    lines = get_lines("input_08.txt")
    antennas, p_max = parse_input(lines)
    print("Part 1:", part_1(antennas, p_max))
    print("Part 2:", part_2(antennas, p_max))


if __name__ == '__main__':
    main()
