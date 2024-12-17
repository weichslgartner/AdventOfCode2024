from typing import Dict, List, Optional

from aoc import input_as_str, extract_all_ints


def parse_input(input_str: str) -> (Dict[str, int], List[int]):
    regs = {}
    registers, program = input_str.split("\n\n")
    for line in registers.splitlines():
        tokens = line.split()
        regs[tokens[1][0]] = int(tokens[-1])
    return regs, extract_all_ints(program)


def get_combo(operand: int, regs: Dict[str, int]) -> int:
    if operand <= 3:
        return operand
    if operand == 4:
        return regs["A"]
    if operand == 5:
        return regs["B"]
    if operand == 6:
        return regs["C"]


def part_1(regs: Dict[str, int], program: List[int]) -> str:
    out = run_program(program, regs)
    return ','.join(map(str, out))


def run_program(program: List[int], regs: Dict[str, int]) -> List[int]:
    inst_ptr = 0
    out = []
    while inst_ptr < len(program):
        opcode, operand = program[inst_ptr:inst_ptr + 2]
        # print(opcode, operand)
        jumps = False
        match opcode:
            case 0:
                regs['A'] = int(regs['A'] / (2 ** get_combo(operand, regs)))
            case 1:
                regs['B'] ^= operand
            case 2:
                regs['B'] = get_combo(operand, regs) % 8
            case 3:
                if regs['A'] != 0:
                    inst_ptr = operand
                    jumps = True
            case 4:
                regs['B'] ^= regs['C']
            case 5:
                out.append(get_combo(operand, regs) % 8)
            case 6:
                regs['B'] = int(regs['A'] / (2 ** get_combo(operand, regs)))
            case 7:
                regs['C'] = int(regs['A'] / (2 ** get_combo(operand, regs)))
        # print(regs)
        inst_ptr = inst_ptr + 2 if not jumps else inst_ptr
    return out


def dfs(reg_a: int, regs: Dict[str, int], program: List[int]) -> Optional[int]:
    regs_before = regs.copy()
    for i in range(8):
        a = reg_a + i
        regs = {'A': a, 'B': regs_before['B'], 'C': regs_before['C']}
        out = run_program(program, regs)
        if out == program:
            return a
        if out[0] == program[-len(out)] and (res := dfs(8 * a, regs_before, program)) is not None:
            return res
    return None


def part_2(regs: Dict[str, int], program: List[int]) -> int:
    return dfs(0, regs, program)


def main():
    input_str = input_as_str("input_17.txt")
    regs, program = parse_input(input_str)
    print("Part 1:", part_1(regs, program))
    print("Part 2:", part_2(regs, program))


if __name__ == '__main__':
    main()
