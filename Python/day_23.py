import collections

from aoc import get_lines


def parse_input(lines):
    connections = collections.defaultdict(list)
    for line in lines:
        src, dst = line.split("-", maxsplit=1)
        connections[src].append(dst)
        connections[dst].append(src)
    return connections


def part_1(three_way):
    return len(list(filter(lambda node: any(node.startswith('t') for node in node.split(","))
                           , three_way)))


def get_three_way_cliques(connections):
    three_way = set()
    for src, dsts in connections.items():
        for d in dsts:
            for c in connections[d]:
                if c in dsts:
                    group = ','.join(sorted([c, d, src]))
                    three_way.add(group)
    return three_way


def can_add(group, candidate, connections):
    for g in group:
        if candidate not in connections[g]:
            return False
    return True


def part_2(three_way, connections):
    biggest_group = []
    for group_str in three_way:
        group = group_str.split(",")
        for g in connections[group[0]]:
            if can_add(group[1:], g, connections):
                group.append(g)
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
