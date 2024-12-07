use std::ops::{Add, Mul};

fn parse_input(input: &str) -> Vec<Vec<u64>> {
    input
        .lines()
        .map(|line| {
            line.split(|c: char| [' ', ':'].contains(&c))
                .filter(|x| !x.is_empty())
                .map(|m| m.parse::<u64>().unwrap())
                .collect()
        })
        .collect()
}

fn concat(a: u64, b: u64) -> u64 {
    let combined = format!("{}{}", a, b);
    combined.parse::<u64>().unwrap()
}

fn can_be_solved(cur: u64, numbers: &Vec<u64>, idx: usize, ops: &Vec<fn(u64, u64) -> u64>) -> bool {
    if idx == numbers.len() - 1 {
        return cur == numbers[0];
    }
    if cur > numbers[0] {
        return false;
    }
    let next_el = numbers[idx + 1];
    for op in ops {
        if can_be_solved(op(cur, next_el), numbers, idx + 1, ops) {
            return true;
        }
    }
    false
}

fn part_1(lines: &[Vec<u64>]) -> u64 {
    lines
        .iter()
        .filter(|line| {
            can_be_solved(line[1], line, 1, &vec![u64::add, u64::mul])
        })
        .map(|line| line[0])
        .sum()
}

fn part_2(lines: &[Vec<u64>]) -> u64 {
    lines
        .iter()
        .filter(|line| {
            can_be_solved(line[1], line, 1, & vec![u64::add, u64::mul, concat])
        })
        .map(|line| line[0])
        .sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_07.txt");
    let parsed_lines = parse_input(input);
    println!("Part 1: {}", part_1(&parsed_lines));
    println!("Part 2: {}", part_2(&parsed_lines));
}
