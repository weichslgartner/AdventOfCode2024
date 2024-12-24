from collections import defaultdict

from aoc import *

class Gate(namedtuple('Gate', 'in1 in2 operator output')):
    def __repr__(self):
        return f'{self.in1} {self.operator} {self.in2} -> {self.output} '


def parse_input(input_str):
    wires = {}
    gates = []
    gates_dict = defaultdict(list)
    wire_lines, gate_lines = input_str.split("\n\n", maxsplit=1)
    for line in wire_lines.splitlines():
        name,value = line.split(":",maxsplit=1)
        wires[name] = int(value.strip())
    for line in gate_lines.splitlines():
        in1,operator,in2,_,output =  line.split(maxsplit=4)
        g = Gate(in1,in2,operator,output)
        gates.append(g)
        gates_dict[g.in1].append(g)
        gates_dict[g.in2].append(g)

    return wires, gates, gates_dict

def calculate(g: Gate, in1, in2):
    match g.operator:
        case "AND":
            return in1 & in2
        case "XOR":
            return in1 ^ in2
        case "OR":
            return in1 | in2


def part_1(wires, gates, gates_dict):
    #print(wires, gates, gates_dict)
    z_wires = {g.output for g in gates if g.output.startswith("z")}
    changed = [w for w in wires.keys() ]
    new_changed = []
    already_fired = set()
    while len(changed) > 0:
        for c in changed:
            for g in gates_dict[c]:
                if g.in1 in wires and g.in2 in wires and g not in already_fired:
                    res = calculate(g,wires[g.in1], wires[g.in2])
                    wires[g.output] = res
                    already_fired.add(g)
                    new_changed.append(g.output)
        changed = new_changed
        if all(z in wires for z in z_wires):
            return calc_z(wires, z_wires)


def calc_z(wires, z_wires):
    res = 0
    for z in z_wires:
        res += wires[z] << int(z[1:])
    return res


def part_2(wires, gates, gates_dict):
    pass


def main():
    input_str = input_as_str("input_24.txt")
    wires, gates, gates_dict = parse_input(input_str)
    print("Part 1:", part_1(wires, gates, gates_dict))
    print("Part 2:", part_2(wires, gates, gates_dict))


if __name__ == '__main__':
    main()
