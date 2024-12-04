from aoc import get_lines, Point


def parse_input(lines):
    return [[c for c in l] for l in lines]


def part_1(grid):
    to_find = "XMAS"
    l = len(to_find)
    cnt = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # horizontal
            if x + l <= len(grid[0]) and to_find == ''.join(grid[y][x + i] for i in range(l)):
                cnt += 1
            if x + 1 >= l and to_find == ''.join(grid[y][x - i] for i in range(l)):
                cnt += 1

            # vertical
            if y + l <= len(grid) and to_find == ''.join(grid[y + i][x] for i in range(l)):
                cnt += 1
            if y + 1 >= l and to_find == ''.join(grid[y - i][x] for i in range(l)):
                cnt += 1

            # diagonal
            if y + l <= len(grid) and x + l <= len(grid[0]) and to_find == ''.join(
                    grid[y + i][x + i] for i in range(l)):
                cnt += 1
            if y + 1 >= l and x + l <= len(grid[0]) and to_find == ''.join(grid[y - i][x + i] for i in range(l)):
                cnt += 1
            if y + l <= len(grid) and x + 1 >= l and to_find == ''.join(grid[y + i][x - i] for i in range(l)):
                cnt += 1
            if y + 1 >= l and x + 1 >= l and to_find == ''.join(grid[y - i][x - i] for i in range(l)):
                cnt += 1

    return cnt


def print_debug(debug):
    for y in range(len(debug)):
        for x in range(len(debug[y])):
            print(debug[y][x], end="")
        print()


def part_2(grid):
    to_find = "MAS"
    l = len(to_find)
    cnt = 0
    for y in range(len(grid) - len(to_find) + 1):
        for x in range(len(grid[0]) - len(to_find) + 1):
            diag1 = ''.join(grid[y + i][x + i] for i in range(l))
            diag2 = ''.join(grid[y + i][x + l - 1 - i] for i in range(l))
            if (diag1 == to_find or diag1[::-1] == to_find) and (diag2 == to_find or diag2[::-1] == to_find):
                cnt += 1
    return cnt


def main():
    lines = get_lines("input_04.txt")
    grid = parse_input(lines)
    print("Part 1:", part_1(grid))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
