from aoc import get_lines


def parse_input(lines):
    return [int(line) for line in lines]


def do_operations(secret_number, rounds=2000):
    for _ in range(rounds):
        secret_number = (secret_number ^ secret_number * 64) % 16777216
        secret_number = (secret_number ^ (secret_number // 32)) % 16777216
        secret_number = (secret_number ^ (secret_number * 2048)) % 16777216
    return secret_number


def part_1(numbers):
    return sum(do_operations(n) for n in numbers)


def part_2(numbers):
    pass


def main():
    lines = get_lines("input_22.txt")
    numbers = parse_input(lines)
    print("Part 1:", part_1(numbers))
    print("Part 2:", part_2(numbers))


if __name__ == '__main__':
    main()
