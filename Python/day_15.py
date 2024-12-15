from typing import Set

from aoc import *

max_x = 0
max_y = 0


def parse_input(input_str: str):
    robot = None
    walls = set()
    boxes = set()
    directions = []
    global max_x, max_y
    grid, directions_str = input_str.split("\n\n", maxsplit=2)
    for y, line in enumerate(grid.splitlines()):
        for x, c in enumerate(line):
            p = Point(x, y)
            max_x = max(max_x, x)
            if c == "#":
                walls.add(p)
            elif c == "@":
                robot = p
            elif c == "O":
                boxes.add(p)
        max_y = max(max_y, y)
    for line in directions_str.splitlines():
        for c in line:
            directions.append(DirectionStr(c))
    return walls, boxes, robot, directions


def part_1(walls: Set[Point], boxes: Set[Point], robot: Point, directions: List[DirectionStr]) -> int:
    return move(walls, boxes, set(), robot, directions)


def move(walls: Set[Point], boxes_left: Set[Point], boxes_right: Set[Point], robot: Point,
         directions: List[DirectionStr]) -> int:
    print_grid(boxes_left, boxes_right, None, robot, walls)

    for direct in directions:
        p = dir_str_to_point(direct)
        robot_next = Point(robot.x + p.x, robot.y + p.y)
        if robot_next in walls:
            print_grid(boxes_left, boxes_right, direct, robot, walls)
            continue
        if not (robot_next not in boxes_left or robot_next not in boxes_right):
            robot = robot_next
            print_grid(boxes_left, boxes_right, direct, robot, walls)
            continue
        left_old = boxes_left.copy()
        right_old = boxes_right.copy()
        to_add_left, to_add_right, to_remove_left, to_remove_right = add_boxes(boxes_left, boxes_right, p, robot_next)
        boxes_left -= to_remove_left
        boxes_right -= to_remove_right
        while True:
            # to_add.add(box_next)
            # we can move
            if (to_add_left | to_add_right).isdisjoint(walls | boxes_left | boxes_right):
                boxes_right |= to_add_right
                boxes_left |= to_add_left
                robot = robot_next
                break
            # only boxes, cannot move
            if not (boxes_left | boxes_right | to_add_right | to_add_left).isdisjoint(walls):
                # revert
                boxes_left = left_old
                boxes_right = right_old
                break
            to_add_left_tmp, to_add_right_tmp, to_remove_left_tmp, to_remove_right_tmp = set(), set(), set(), set()
            for s in [to_add_left.copy(), to_add_right.copy()]:
                for b in s:
                    to_add_left_new, to_add_right_new, to_remove_left_new, to_remove_right_new = add_boxes(boxes_left,
                                                                                                           boxes_right,
                                                                                                           p,
                                                                                                           Point(b.x,
                                                                                                                 b.y))
                    to_add_left_tmp |= to_add_left_new
                    to_add_right_tmp |= to_add_right_new
                    to_remove_left_tmp |= to_remove_left_new
                    to_remove_right_tmp |= to_remove_right_new
            to_add_left |= to_add_left_tmp
            to_add_right |= to_add_right_tmp
            boxes_left -= to_remove_left_tmp
            boxes_right -= to_remove_right_tmp
        print_grid(boxes_left, boxes_right, direct, robot, walls)
    return sum(100 * p.y + p.x for p in boxes_left)


def add_boxes(boxes_left, boxes_right, p, robot_next):
    if robot_next in boxes_left:
        to_remove_left = {robot_next}
        to_remove_right = {Point(x=robot_next.x + 1, y=robot_next.y)}
        to_add_left = {Point(robot_next.x + p.x, robot_next.y + p.y)}
        to_add_right = {Point(robot_next.x + 1 + p.x, robot_next.y + p.y)}
        return to_add_left, to_add_right, to_remove_left, to_remove_right
    elif robot_next in boxes_right:
        to_remove_right = {robot_next}
        to_remove_left = {Point(x=robot_next.x - 1, y=robot_next.y)}
        to_add_left = {Point(robot_next.x - 1 + p.x, robot_next.y + p.y)}
        to_add_right = {Point(robot_next.x + p.x, robot_next.y + p.y)}
        return to_add_left, to_add_right, to_remove_left, to_remove_right
    return set(), set(), set(), set()


def print_grid(boxes_left, boxes_right, direct, robot, walls):
    return
    print("Direction ", direct)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            p = Point(x, y)
            if p in walls:
                print("#", end="")
            elif p in boxes_left:
                print("[", end="")
            elif p in boxes_right:
                print("]", end="")
            elif p == robot:
                print("@", end="")
            else:
                print(".", end="")
        print()


def part_2(walls, boxes, robot, directions):
    new_walls, new_boxes_left, new_boxes_right = set(), set(), set()
    for w in walls:
        w_new = Point(x=w.x * 2, y=w.y)
        new_walls.add(w_new)
        new_walls.add(Point(w_new.x + 1, w.y))
    for b in boxes:
        b_new = Point(x=b.x * 2, y=b.y)
        new_boxes_left.add(b_new)
        new_boxes_right.add(Point(b_new.x + 1, b.y))
    new_robot = Point(x=robot.x * 2, y=robot.y)
    global max_x
    max_x *= 2
    return move(new_walls, new_boxes_left, new_boxes_right, new_robot, directions)


def main():
    lines = input_as_str("input_15.txt")
    walls, boxes, robot, directions = parse_input(lines)
    print("Part 1:", part_1(walls, boxes.copy(), robot, directions))
    print("Part 2:", part_2(walls, boxes, robot, directions))


if __name__ == '__main__':
    main()
