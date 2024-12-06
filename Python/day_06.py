from aoc import *


def parse_input(lines):
    obstacles = set()
    start = None
    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            if c == "#":
                obstacles.add(Point(x=x,y=y))
            elif c == "^":
                start = Point(x,y)

    return obstacles,start,Point(x=len(lines[0]),y=len(lines))


def part_1(obstacles, start, maxP ):
    cur = start
    visited = set()
    dir = Direction.NORTH
    while 0 <= cur.x < maxP.x and 0 <= cur.y < maxP.y:
        next = dir_to_point(dir)
        nextP = Point(x=cur.x+next.x, y=cur.y+next.y)
        while nextP in obstacles:
            dir = Direction((dir.value+1) % (len(Direction)))
            next = dir_to_point(dir)
            nextP = Point(x=cur.x + next.x, y=cur.y + next.y)
        visited.add(cur)
        cur = nextP
    #print_grid(maxP, obstacles, visited)
    return len(visited)


def print_grid(maxP, obstacles, visited):
    for y in range(maxP.y):
        for x in range(maxP.x):
            p = Point(x, y)
            if p in obstacles:
                print("#", end="")
            elif p in visited:
                print("X", end="")
            else:
                print(".", end="")
        print()


def part_2(obstacles, start, maxP ):
    cur = start
    visited = set()
    visited_dir = set()
    new_obstacles = set()
    dir = Direction.NORTH
    while 0 <= cur.x < maxP.x and 0 <= cur.y < maxP.y:
        dir_, nextP = get_next_point(cur, dir, obstacles)
        obstacles.add(nextP)
        if has_loops(cur, dir, maxP, obstacles, visited_dir.copy()):
            new_obstacles.add(nextP)
        visited_dir.add((cur, dir))
        obstacles.remove(nextP)
        cur = nextP
        dir = dir_
    #print_grid(maxP, obstacles, visited)
    return len(new_obstacles)


def has_loops(cur, dir, maxP, obstacles, visited_dir):
    while 0 <= cur.x < maxP.x and 0 <= cur.y < maxP.y:
        if (cur, dir) in visited_dir:
            return True
        visited_dir.add((cur, dir))
        dir, nextP = get_next_point(cur, dir, obstacles)
        cur = nextP
    return False


def get_next_point(cur, dir, obstacles):
    next = dir_to_point(dir)
    nextP = Point(x=cur.x + next.x, y=cur.y + next.y)
    while nextP in obstacles:
        dir = Direction((dir.value + 1) % (len(Direction)))
        next = dir_to_point(dir)
        nextP = Point(x=cur.x + next.x, y=cur.y + next.y)
    return dir, nextP


def main():
    lines = get_lines("input_06.txt") # too low 1696 #too high 1922
    obstacles, start, maxP = parse_input(lines)
    print("Part 1:", part_1(obstacles, start, maxP ))
    print("Part 2:", part_2(obstacles, start, maxP ))


if __name__ == '__main__':
    main()
