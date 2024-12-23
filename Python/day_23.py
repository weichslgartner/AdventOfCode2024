import collections
from typing import Dict, List, Set

from aoc import get_lines


def parse_input(lines: List[str]) -> Dict[str, List[str]]:
    connections = collections.defaultdict(list)
    for line in lines:
        src, dst = line.split("-", maxsplit=1)
        connections[src].append(dst)
        connections[dst].append(src)
    return connections


def get_three_way_cliques(connections: Dict[str, List[str]]) -> Set[str]:
    three_way = set()
    for src, dsts in connections.items():
        for d in dsts:
            for c in connections[d]:
                if c in dsts:
                    group = ','.join(sorted([c, d, src]))
                    three_way.add(group)
    return three_way


def can_add(group: List[str], candidate: str, connections: Dict[str, List[str]]) -> bool:
    for g in group:
        if candidate not in connections[g]:
            return False
    return True


def part_1(three_way: Set[str]) -> int:
    return len(list(filter(lambda node: any(node.startswith('t') for node in node.split(",")),
                           three_way)))


def part_2(three_way: Set[str], connections: Dict[str, List[str]]) -> str:
    biggest_group = []
    for group_str in three_way:
        group = group_str.split(",")
        for candidate in filter(lambda x: x not in group, connections[group[0]]):
            if can_add(group[1:], candidate, connections):
                group.append(candidate)
            if len(group) > len(biggest_group):
                biggest_group = group.copy()
    return ','.join(sorted(biggest_group))


def main():
    lines = get_lines("input_23.txt")
    connections = parse_input(lines)
    three_way = get_three_way_cliques(connections)
    print("Part 1:", part_1(three_way))
    print("Part 2:", part_2(three_way, connections))


if __name__ == '__main__':
    main()
