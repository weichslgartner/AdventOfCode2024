from typing import Dict, List

from aoc import Point, get_lines, get_neighbours_4


def parse_input(lines: List[str]) -> (Dict[Point, int], List[Point], Point):
    points = {}
    starts = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                points[Point(x, y)] = int(c)
            if c == '0':
                starts.append(Point(x, y))
    return points, starts, Point(x=len(lines[0]), y=len(lines))


def solve(points: Dict[Point, int], starts: List[Point], p_max: Point) -> (int, int):
    return tuple(sum(x) for x in zip(*map(lambda p: get_n_trailheads(p, p_max, points), starts)))


def get_n_trailheads(p: Point, p_max: Point, points: Dict[Point, int]) -> (int, int):
    cur, next_ps = [p], []
    heads = set()
    score = 0
    while len(cur) > 0:
        for p in cur:
            for n in filter(lambda x: x in points and points[x] - points[p] == 1, get_neighbours_4(p, p_max)):
                if points[n] == 9:
                    heads.add(n)
                    score += 1
                else:
                    next_ps.append(n)
        cur, next_ps = next_ps, []
    return len(heads), score


def main():
    lines = get_lines("input_10.txt")
    points, starts, p_max = parse_input(lines)
    part1, part2 = solve(points, starts, p_max)
    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == '__main__':
    main()
