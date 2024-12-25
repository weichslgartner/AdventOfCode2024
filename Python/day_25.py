from typing import List

from aoc import input_as_str

KEY_WIDTH = 5
KEY_HEIGHT = 5


def parse_input(input_str: str) -> (List[int], List[int]):
    blocks = input_str.split("\n\n")
    keys, locks = [], []

    for block in blocks:
        current = [-1] * KEY_WIDTH
        is_key = block[0] == "#"
        for y, line in enumerate(block.splitlines()):
            for x, c in enumerate(line):
                if is_key and c == '.' and current[x] == -1:
                    current[x] = y - 1
                if not is_key and c == '.':
                    current[x] = KEY_HEIGHT - y
        if is_key:
            keys.append(current)
        else:
            locks.append(current)
    return keys, locks


def does_fit(key: List[int], lock: List[int]) -> bool:
    for k, l in zip(key, lock):
        if k + l > KEY_HEIGHT:
            return False
    return True


def part_1(keys: List[int], locks: List[int]) -> int:
    return sum(does_fit(key, lock) for key in keys for lock in locks)


def main():
    lines = input_as_str("input_25.txt")
    keys, locks = parse_input(lines)
    print("Part 1:", part_1(keys, locks))


if __name__ == '__main__':
    main()
