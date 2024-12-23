import collections

from aoc import get_lines


def parse_input(lines):
    connections = collections.defaultdict(list)
    for line in lines:
        src, dst = line.split("-",maxsplit=1)
        connections[src].append(dst)
        connections[dst].append(src)
    return connections


def part_1(connections):
    print(connections)
    three_way = set()
    for src, dsts in connections.items():
        for d in dsts:
            for c in connections[d]:
                if c in dsts:
                    group = ','.join(sorted([c,d,src]))
                    if c.startswith("t") or d.startswith("t") or src.startswith("t"):
                        three_way.add(group)
    print(three_way)
    return len(three_way)



def part_2(connections):
    pass


def main():
    lines = get_lines("input_23.txt") # too high 2316
    connections = parse_input(lines)
    print("Part 1:", part_1(connections))
    print("Part 2:", part_2(connections))


if __name__ == '__main__':
    main()
