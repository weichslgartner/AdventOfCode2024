use std::collections::HashMap;

fn parse_input(input_str: &str) -> (HashMap<char, i64>, Vec<i64>) {
    let mut regs = HashMap::new();
    let parts: Vec<&str> = input_str.split("\n\n").collect();
    let registers = parts[0];
    let program = parts[1];

    for line in registers.lines() {
        let tokens: Vec<&str> = line.split_whitespace().collect();
        let key = tokens[1].chars().next().unwrap();
        let value = tokens.last().unwrap().parse::<i64>().unwrap();
        regs.insert(key, value);
    }
    let (_title, insts) = program.split_once(" ").unwrap();
    let program: Vec<i64> = insts
        .trim()
        .split(",")
        .map(|x| {
            x.parse::<i64>()
                .unwrap_or_else(|_| panic!("cannot convert {}", x))
        })
        .collect();

    (regs, program)
}

fn get_combo(operand: i64, regs: &HashMap<char, i64>) -> i64 {
    match operand {
        0..=3 => operand,
        4 => *regs.get(&'A').unwrap_or(&0),
        5 => *regs.get(&'B').unwrap_or(&0),
        6 => *regs.get(&'C').unwrap_or(&0),
        _ => 0,
    }
}

fn run_program(program: &[i64], regs: &mut HashMap<char, i64>) -> Vec<i64> {
    let mut inst_ptr = 0;
    let mut out = Vec::new();

    while inst_ptr < program.len() {
        let opcode = program[inst_ptr];
        let operand = program[inst_ptr + 1];
        let mut jumps = false;
        let combo = get_combo(operand, regs);
        match opcode {
            0 => {
                if let Some(a) = regs.get_mut(&'A') {
                    *a /= 2_i64.pow(combo as u32);
                }
            }
            1 => {
                if let Some(b) = regs.get_mut(&'B') {
                    *b ^= operand;
                }
            }
            2 => {
                if let Some(b) = regs.get_mut(&'B') {
                    *b = combo % 8;
                }
            }
            3 => {
                if regs.get(&'A').unwrap_or(&0) != &0 {
                    inst_ptr = operand as usize;
                    jumps = true;
                }
            }
            4 => {
                let c = *regs.get(&'C').unwrap();
                if let Some(b) = regs.get_mut(&'B') {
                    *b ^= c;
                }
            }
            5 => {
                out.push(get_combo(operand, regs) % 8);
            }
            6 => {
                let a = *regs.get(&'A').unwrap();
                if let Some(b) = regs.get_mut(&'B') {
                    *b = a / 2_i64.pow(combo as u32);
                }
            }
            7 => {
                let a = *regs.get(&'A').unwrap();
                if let Some(c) = regs.get_mut(&'C') {
                    *c = a / 2_i64.pow(combo as u32);
                }
            }
            _ => {}
        }

        if !jumps {
            inst_ptr += 2;
        }
    }
    out
}

fn dfs(reg_a: i64, regs: &HashMap<char, i64>, program: &[i64]) -> Option<i64> {
    let regs_before = regs.clone();
    for i in 0..8 {
        let a = reg_a + i;
        let mut updated_regs = HashMap::new();
        updated_regs.insert('A', a);
        updated_regs.insert('B', *regs_before.get(&'B').unwrap_or(&0));
        updated_regs.insert('C', *regs_before.get(&'C').unwrap_or(&0));

        let out = run_program(program, &mut updated_regs);
        if out == program {
            return Some(a);
        }
        if program.ends_with(&out) {
            if let Some(res) = dfs(8 * a, &regs_before, program) {
                return Some(res);
            }
        }
    }
    None
}

fn part_1(regs: &mut HashMap<char, i64>, program: &[i64]) -> String {
    let out = run_program(program, regs);
    out.iter()
        .map(|x| x.to_string())
        .collect::<Vec<_>>()
        .join(",")
}

fn part_2(regs: &HashMap<char, i64>, program: &Vec<i64>) -> i64 {
    dfs(0, regs, program).unwrap_or_default()
}

fn main() {
    let input_str = include_str!("../../../inputs/input_17.txt");
    let (mut regs, program) = parse_input(input_str);
    println!("Part 1: {}", part_1(&mut regs, &program));
    println!("Part 2: {}", part_2(&regs, &program));
}
