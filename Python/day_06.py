from typing import Set

from aoc import *


def parse_input(lines: List[str]) -> (Set[Point], Point, Point):
    obstacles = set()
    start = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                obstacles.add(Point(x=x, y=y))
            elif c == "^":
                start = Point(x, y)

    return obstacles, start, Point(x=len(lines[0]), y=len(lines))


def part_1(obstacles: Set[Point], start: Point, max_p: Point) -> int:
    cur = start
    visited = set()
    direction = Direction.NORTH
    while 0 <= cur.x < max_p.x and 0 <= cur.y < max_p.y:
        visited.add(cur)
        direction, cur = get_next_point(cur, direction, obstacles)
    return len(visited)


def part_2(obstacles: Set[Point], start: Point, max_p: Point) -> int:
    cur = start
    new_obstacles = set()
    direction = Direction.NORTH
    while 0 <= cur.x < max_p.x and 0 <= cur.y < max_p.y:
        dir_, next_p = get_next_point(cur, direction, obstacles)
        if next_p not in obstacles and next_p not in new_obstacles and next_p != start:
            obstacles.add(next_p)
            if has_loops(start, Direction.NORTH, max_p, obstacles):
                new_obstacles.add(next_p)
            obstacles.remove(next_p)
        cur = next_p
        direction = dir_
    return len(new_obstacles)


def has_loops(cur: Point, direction: Direction, max_p: Point, obstacles: Set[Point]) -> bool:
    visited_dir = set()
    while 0 <= cur.x < max_p.x and 0 <= cur.y < max_p.y:
        if (cur, direction) in visited_dir:
            return True
        visited_dir.add((cur, direction))
        direction, cur = get_next_point(cur, direction, obstacles)
    return False


def get_next_point(cur: Point, direction: Direction, obstacles: Set[Point]) -> (Direction, Point):
    next_dir = dir_to_point(direction)
    next_p = Point(x=cur.x + next_dir.x, y=cur.y + next_dir.y)
    while next_p in obstacles:
        direction = Direction((direction.value + 1) % (len(Direction)))
        next_dir = dir_to_point(direction)
        next_p = Point(x=cur.x + next_dir.x, y=cur.y + next_dir.y)
    return direction, next_p


def main():
    lines = get_lines("input_06.txt")  # too low 1696 #too high 1922
    obstacles, start, max_p = parse_input(lines)
    print("Part 1:", part_1(obstacles, start, max_p))
    print("Part 2:", part_2(obstacles, start, max_p))


if __name__ == '__main__':
    main()
