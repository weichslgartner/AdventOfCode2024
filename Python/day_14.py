from collections import Counter
from math import prod
from typing import List, Tuple

from aoc import get_lines, extract_all_ints, Point

WIDTH = 101
HEIGHT = 103


def parse_input(lines: List[str]) -> List[Tuple[Point, Point]]:
    return [(Point(*ps[:2]), Point(*ps[2:])) for line in lines for ps in [extract_all_ints(line)]]


def part_1(points: List[Tuple[Point, Point]], steps: int = 100) -> int:
    return prod(calc_quads(perform_movement(points, steps)))


def perform_movement(points: List[Tuple[Point, Point]], steps: int = 1) -> List[Tuple[Point, Point]]:
    return [(Point(x=(p[0].x + p[1].x * steps) % WIDTH, y=(p[0].y + p[1].y * steps) % HEIGHT), p[1]) for p in points]


def is_christmas_tree(points: List[Tuple[Point, Point]]) -> bool:
    return all(v == 1 for v in Counter(map(lambda p: p[0], points)).values())


def debug(i: int, points: List[Tuple[Point, Point]]):
    if not is_christmas_tree(points):
        return
    print(i, "=========")
    christmas_tree = {map(lambda p_: p_[0], points)}
    for y in range(HEIGHT):
        for x in range(WIDTH):
            p = Point(x, y)
            if p in christmas_tree:
                print("1", end="")
            else:
                print(".", end="")
        print()


def calc_quads(points: List[Tuple[Point, Point]]) -> List[int]:
    quads = [0] * 4
    for p, _ in points:
        match (p.y < HEIGHT // 2, p.y > HEIGHT // 2, p.x < WIDTH // 2, p.x > WIDTH // 2):
            case (True, _, True, _):  # Top-left
                quads[0] += 1
            case (True, _, _, True):  # Top-right
                quads[1] += 1
            case (_, True, True, _):  # Bottom-left
                quads[2] += 1
            case (_, True, _, True):  # Bottom-right
                quads[3] += 1
            case _:  # Ignore points on boundaries
                pass
    return quads

def part_2(points: List[Tuple[Point, Point]]) -> int:
    for i in range(1_000_000):
        if is_christmas_tree(points):
            return i
        points = perform_movement(points, 1)


def main():
    lines = get_lines("input_14.txt")
    points = parse_input(lines)
    print("Part 1:", part_1(points.copy()))
    print("Part 2:", part_2(points))


if __name__ == '__main__':
    main()
