from typing import List

from aoc import input_as_str


def parse_input(disk_map: str) -> List:
    id = 0
    res = []
    is_id = True
    free_space = {}
    blocks = {}
    for c in disk_map:
        if is_id:
            blocks[len(res)] = int(c)
            for _ in range(int(c)):
                res.append(id)
            id += 1
        else:
            free_space[len(res)] = int(c)
            for _ in range(int(c)):
                res.append('.')
        is_id = not is_id
    return res, free_space, blocks


def checksum(disk):
    return sum(i * c if c != '.' else 0 for i, c in enumerate(disk))


def part_1(disk_map):
    l = disk_map.index('.')
    r = len(disk_map) - 1
    assert disk_map[r] != '.'
    while l <= r:
        disk_map[l], disk_map[r] = disk_map[r], disk_map[l]
        l = disk_map.index('.', l + 1)
        r -= 1
        while disk_map[r] == '.':
            r -= 1
    return checksum(disk_map)


def part_2(disk_map, free_space: dict, blocks: dict):
    for idx, l in reversed(blocks.items()):
        target = 0
        keys = sorted(free_space.keys())
        while target < len(keys) and l > free_space[keys[target]]:
            target += 1
        if target < len(keys) and idx > keys[target]:
            disk_map[keys[target]:keys[target] + l], disk_map[idx:idx + l] = disk_map[idx:idx + l], disk_map[
                                                                                                    keys[target]:keys[
                                                                                                        target] + l]
            if free_space[keys[target]] > l:
                free_space[keys[target] + l] = free_space[keys[target]] - l
            del free_space[keys[target]]
    return checksum(disk_map)


def main():
    lines = input_as_str("input_09.txt")
    disk_map, free_space, blocks = parse_input(lines)
    print("Part 1:", part_1(disk_map.copy()))
    print("Part 2:", part_2(disk_map, free_space, blocks))  # 8509897721111 too high


if __name__ == '__main__':
    main()
