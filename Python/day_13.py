from typing import List

from aoc import input_as_str, extract_all_ints, Point

COST_A = 3
COST_B = 1
OFFSET = 10000000000000


def parse_input(input_str: str) -> List[List[Point]]:
    machines = []
    for block in input_str.split("\n\n"):
        machine = []
        for line in block.splitlines():
            nums = extract_all_ints(line)
            machine.append(Point(x=nums[0], y=nums[1]))
        machines.append(machine)
    return machines


def solve(a: Point, b: Point, target: Point) -> int:
    target_diff = target.x * b.y - target.y * b.x
    dividend = (b.y * a.x - b.x * a.y)
    if target_diff % dividend != 0:
        return 0
    a_times = int(target_diff / dividend)
    b_times = int((target.y - a_times * a.y) / b.y)
    return a_times * COST_A + b_times * COST_B


def part_1(machines):
    return sum(solve(a, b, target=target) for a, b, target in machines)


def part_2(machines):
    return sum(solve(a, b, target=Point(target.x + OFFSET, target.y + OFFSET)) for a, b, target in machines)


def main():
    lines = input_as_str("input_13.txt")
    machines = parse_input(lines)
    print("Part 1:", part_1(machines))
    print("Part 2:", part_2(machines))


if __name__ == '__main__':
    main()
