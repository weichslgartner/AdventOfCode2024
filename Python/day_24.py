from collections import defaultdict

import netgraph
import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_agraph import write_dot

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
        name, value = line.split(":", maxsplit=1)
        wires[name] = int(value.strip())
    for line in gate_lines.splitlines():
        in1, operator, in2, _, output = line.split(maxsplit=4)
        g = Gate(in1, in2, operator, output)
        gates.append(g)
        gates_dict[g.in1].append(g)
        gates_dict[g.in2].append(g)
    return wires, gates, gates_dict

def is_correct_adder(output,carry_in):
    return True

def calculate(g: Gate, in1, in2):
    match g.operator:
        case "AND":
            return in1 & in2
        case "XOR":
            return in1 ^ in2
        case "OR":
            return in1 | in2


def part_1(wires, gates, gates_dict):
    # print(wires, gates, gates_dict)
    z_wires = {g.output for g in gates if g.output.startswith("z")}
    changed = [w for w in wires.keys()]
    new_changed = []
    already_fired = set()
    while len(changed) > 0:
        for c in changed:
            for g in gates_dict[c]:
                if g.in1 in wires and g.in2 in wires and g not in already_fired:
                    res = calculate(g, wires[g.in1], wires[g.in2])
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


def part_2(wires, gates: List[Gate], gates_dict):
    z_wires = sorted(g.output for g in gates if g.output.startswith("z"))
    connections = defaultdict(list)
    for g in gates:
        connections[g.output]+= [g.in1,g.in2]
    for z in z_wires:
        predecessors = {z for z in connections[z]}
        new_queue = []
        queue = [z for z in connections[z]]
        while len(queue) > 0:
            for q in queue:
                for n in connections[q]:
                    new_queue.append(n)
                    predecessors.add(n)
            queue, new_queue = new_queue, []
        print(z, predecessors)
        print({g for p in predecessors for g in gates_dict[p]})
        for p in predecessors:
            if (p.startswith("x") or p.startswith("y")) and int(p[1:]) > int(z[1:]):
                print("offending",p,z,int(p[1:]),int(z[1:]))

    print(z_wires)

    show_layout(gates)
    # lösen durch hinschauen
    return ','.join(sorted(["z12", "djg", "z19", "sbg", "mcq", "hjm", "dsd", "z37"]))

def show_layout(gates):
    edges = []
    G = nx.DiGraph()
    for g in gates:
        gate_node = f"{g.in1}{g.operator}{g.in2}"
        G.add_node(gate_node, gate=True)
        # Connect inputs to the gate node
        G.add_edge(g.in1, gate_node)
        G.add_edge(g.in2, gate_node)
        G.add_edge(gate_node, g.output)
    try:
        #pos =  nx.multipartite_layout(G)
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")  # Requires pygraphviz or pydot
    except ImportError:
        print("Install pygraphviz or pydot for better layouts. Falling back to spring layout.")
        pos = nx.spring_layout(G)
    write_dot(G,"graph.dot")

    #pos = nx.spring_layout(G)
    # Draw the graph


    nx.draw(G, pos, with_labels=True, node_size=100, node_color="lightblue", font_size=8,
            edge_color="gray")
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
    plt.title("Logic Gate Network")
    plt.show()


def main():
    input_str = input_as_str("input_24.txt")
    wires, gates, gates_dict = parse_input(input_str)
    print("Part 1:", part_1(wires, gates, gates_dict))
    print("Part 2:", part_2(wires, gates, gates_dict))


if __name__ == '__main__':
    main()
