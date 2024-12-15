from typing import Set, Tuple

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


def move(walls: Set[Point], boxes_left: Set[Point], boxes_right: Set[Point], robot: Point,
         directions: List[DirectionStr]) -> int:
    for direct in directions:
        p = dir_str_to_point(direct)
        robot_next = Point(robot.x + p.x, robot.y + p.y)
        if robot_next in walls:
            continue
        if (robot_next not in boxes_left) and (len(boxes_right) == 0 or robot_next not in boxes_right):
            robot = robot_next
            continue
        boxes_left, boxes_right, robot = move_boxes(boxes_left, boxes_right, p, robot, robot_next, walls)
    return sum(100 * p.y + p.x for p in boxes_left)


def can_move_free(to_add_right: Set[Point], to_add_left: Set[Point], boxes_left: Set[Point], boxes_right: Set[Point],
                  walls: Set[Point]) -> bool:
    for non_free in [boxes_left, boxes_right, walls]:
        for to_add in [to_add_right, to_add_left]:
            if not to_add.isdisjoint(non_free):
                return False
    return True


def move_boxes(boxes_left: Set[Point], boxes_right: Set[Point], p: Point, robot: Point, robot_next: Point,
               walls: Set[Point]) -> Tuple[Set[Point], Set[Point], Point]:
    left_old = boxes_left.copy()
    right_old = boxes_right.copy()
    to_add_left, to_add_right, to_remove_left, to_remove_right = add_boxes(boxes_left, boxes_right, p, robot_next)
    boxes_left -= to_remove_left
    boxes_right -= to_remove_right
    while True:
        # we can move
        if can_move_free(to_add_right, to_add_left, boxes_left, boxes_right, walls):
            boxes_right |= to_add_right
            boxes_left |= to_add_left
            robot = robot_next
            break
        # only boxes, cannot move
        if not to_add_left.isdisjoint(walls) or not to_add_right.isdisjoint(walls):
            # revert
            boxes_left = left_old
            boxes_right = right_old
            break
        for s in [to_add_left.copy(), to_add_right.copy()]:
            for b in s:
                add_l, add_r, rem_l, rem_r = add_boxes(boxes_left, boxes_right, p, Point(b.x, b.y))
                to_add_left |= add_l
                to_add_right |= add_r
                boxes_left -= rem_l
                boxes_right -= rem_r
    return boxes_left, boxes_right, robot


def add_boxes(boxes_left: Set[Point], boxes_right: Set[Point], p: Point, robot_next: Point) \
        -> Tuple[Set[Point], Set[Point], Set[Point], Set[Point]]:
    if robot_next in boxes_left:
        to_remove_left = {robot_next}
        to_remove_right = {Point(x=robot_next.x + 1, y=robot_next.y)} if len(boxes_right) > 0 else set()
        to_add_left = {Point(robot_next.x + p.x, robot_next.y + p.y)}
        to_add_right = {Point(robot_next.x + 1 + p.x, robot_next.y + p.y)} if len(boxes_right) > 0 else set()
        return to_add_left, to_add_right, to_remove_left, to_remove_right
    # only used in part2
    elif robot_next in boxes_right:
        to_remove_right = {robot_next}
        to_remove_left = {Point(x=robot_next.x - 1, y=robot_next.y)}
        to_add_left = {Point(robot_next.x - 1 + p.x, robot_next.y + p.y)}
        to_add_right = {Point(robot_next.x + p.x, robot_next.y + p.y)}
        return to_add_left, to_add_right, to_remove_left, to_remove_right
    return set(), set(), set(), set()


def expand(points: Set[Point]) -> Tuple[Set[Point], Set[Point]]:
    left, right = set(), set()
    for p in points:
        b_new = Point(x=p.x * 2, y=p.y)
        left.add(b_new)
        right.add(Point(b_new.x + 1, p.y))
    return left, right


def part_1(walls: Set[Point], boxes: Set[Point], robot: Point, directions: List[DirectionStr]) -> int:
    return move(walls, boxes, set(), robot, directions)


def part_2(walls: Set[Point], boxes: Set[Point], robot: Point, directions: List[DirectionStr]) -> int:
    new_walls_left, new_walls_right = expand(walls)
    new_boxes_left, new_boxes_right = expand(boxes)
    new_robot = Point(x=robot.x * 2, y=robot.y)
    return move(new_walls_left | new_walls_right, new_boxes_left, new_boxes_right, new_robot, directions)


def main():
    lines = input_as_str("input_15.txt")
    walls, boxes, robot, directions = parse_input(lines)
    print("Part 1:", part_1(walls, boxes.copy(), robot, directions))
    print("Part 2:", part_2(walls, boxes, robot, directions))


if __name__ == '__main__':
    main()
