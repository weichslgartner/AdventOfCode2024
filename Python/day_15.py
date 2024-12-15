from typing import Set

from aoc import *


def parse_input(input_str: str):
    robot = None
    walls = set()
    boxes = set()
    directions = []
    grid, directions_str = input_str.split("\n\n", maxsplit=2)
    for y, line in enumerate(grid.splitlines()):
        for x, c in enumerate(line):
            p = Point(x, y)
            if c == "#":
                walls.add(p)
            elif c == "@":
                robot = p
            elif c == "O":
                boxes.add(p)
    for line in directions_str.splitlines():
        for c in line:
            directions.append(DirectionStr(c))
    return walls, boxes, robot, directions


def part_1(walls: Set[Point], boxes: Set[Point], robot: Point, directions: List[DirectionStr]) -> int:
   # print(walls, boxes, robot, directions)
    for direct in directions:
        p = dir_str_to_point(direct)
        robot_next = Point(robot.x + p.x, robot.y+ p.y)
        if robot_next in walls:
            print_grid(boxes, direct, robot, walls)
            continue
        if robot_next not in boxes:
            robot = robot_next
            print_grid(boxes, direct, robot, walls)
            continue
        to_remove = {robot_next}
        to_add = set()
        box_next = Point(robot_next.x + p.x, robot_next.y + p.y)
        while box_next not in walls:
            to_add.add(box_next)
            # we can move
            if box_next not in walls and box_next not in boxes:
                boxes -= to_remove
                boxes |= to_add
                robot = robot_next
                break
            # only boxes, cannot move
            if box_next in walls:
                break
            to_remove.add(box_next)
            box_next = Point(box_next.x + p.x, box_next.y + p.y)
        print_grid(boxes, direct, robot, walls)
    return sum(100 * p.y + p.x for p in boxes)


def print_grid(boxes, direct, robot, walls):
    return
    print("Direction ", direct)
    for y in range(8):
        for x in range(9):
            p = Point(x, y)
            if p in walls:
                print("#", end="")
            elif p in boxes:
                print("O", end="")
            elif p == robot:
                print("@", end="")
            else:
                print(".", end="")
        print()


def part_2(walls, boxes, robot, directions):
    pass


def main():
    lines = input_as_str("input_15.txt")
    walls, boxes, robot, directions = parse_input(lines)
    print("Part 1:", part_1(walls, boxes, robot, directions))
    print("Part 2:", part_2(walls, boxes, robot, directions))


if __name__ == '__main__':
    main()
