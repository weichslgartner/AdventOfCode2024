from typing import List, Dict, Optional

from aoc import input_as_str


def parse_input(disk_map: str) -> (List[int | str], Dict[int, int], Dict[int, int]):
    block_id = 0
    res = []
    is_id = True
    free_space = {}
    blocks = {}
    for c in disk_map:
        if is_id:
            blocks[len(res)] = int(c)
            for _ in range(int(c)):
                res.append(block_id)
            block_id += 1
        else:
            free_space[len(res)] = int(c)
            for _ in range(int(c)):
                res.append('.')
        is_id = not is_id
    return res, free_space, blocks


def checksum(disk: List[int | str]) -> int:
    return sum(i * c if c != '.' else 0 for i, c in enumerate(disk))


def part_1(disk_map: List[int | str]) -> int:
    left = disk_map.index('.')
    right = len(disk_map) - 1
    assert disk_map[right] != '.'
    while left <= right:
        disk_map[left], disk_map[right] = disk_map[right], disk_map[left]
        left = disk_map.index('.', left + 1)
        right -= 1
        while disk_map[right] == '.':
            right -= 1
    return checksum(disk_map)


def find_target(free_space: Dict[int, int], idx: int, keys: List[int], length: int) -> Optional[int]:
    for target, key in enumerate(keys):
        if key <=0:
            continue
        if length <= free_space[key]:
            if idx > key:
                return target
            return None
    return None


def part_2(disk_map: List[int | str], free_space: Dict[int, int], blocks: Dict[int, int]) -> int:
    keys = sorted(free_space.keys())
    for idx, length in reversed(blocks.items()):
        target = find_target(free_space, idx, keys, length)
        if target is not None:
            # swap block with free space
            disk_map[keys[target]:keys[target] + length], disk_map[idx:idx + length] = (
                disk_map[idx:idx + length], disk_map[keys[target]:keys[target] + length])
            if free_space[keys[target]] > length:
                free_space[keys[target] + length] = free_space[keys[target]] - length
                keys[target] = keys[target] + length
            else:
                keys.remove(keys[target])
    return checksum(disk_map)


def main():
    lines = input_as_str("input_09.txt")
    disk_map, free_space, blocks = parse_input(lines)
    print("Part 1:", part_1(disk_map.copy()))
    print("Part 2:", part_2(disk_map, free_space, blocks))  # 8509897721111 too high


if __name__ == '__main__':
    main()
