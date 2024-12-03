use regex::Regex;

#[derive(Debug)]
struct Instruction {
    do_group: bool,
    dont_group: bool,
    mul_group: bool,
    first_num: i32,
    second_num: i32,
}
fn parse_input(line: &str) -> Vec<Instruction> {
    let re = Regex::new(r"(do\(\))|(don't\(\))|(mul\((\d+),(\d+)\))").unwrap();
    re.captures_iter(line)
        .map(|cap| Instruction {
            do_group: cap.get(1).map_or(false, |m| !m.as_str().is_empty()),
            dont_group: cap.get(2).map_or(false, |m| !m.as_str().is_empty()),
            mul_group: cap.get(3).map_or(false, |m| !m.as_str().is_empty()),
            first_num: cap
                .get(4)
                .map_or(0, |m| m.as_str().parse::<i32>().unwrap_or(0)),
            second_num: cap
                .get(5)
                .map_or(0, |m| m.as_str().parse::<i32>().unwrap_or(0))
        })
        .collect()
}

fn part_1(instructions: &[Instruction]) -> i32 {
    instructions
        .iter()
        .filter(|i| i.mul_group)
        .map(|i| i.first_num * i.second_num)
        .sum()
}

fn conditional_mul(state: (bool, i32), el: &Instruction) -> (bool, i32) {
    let (mut enabled, mut total) = state;
    if el.do_group {
        enabled = true;
    } else if el.dont_group {
        enabled = false;
    } else if el.mul_group && enabled {
        total += el.first_num * el.second_num;
    }
    (enabled, total)
}

fn part_2(tups: &[Instruction]) -> i32 {
    tups.iter().fold((true, 0), conditional_mul).1
}

fn main() {
    let line = include_str!("../../../inputs/input_03.txt");
    let tups = parse_input(line);
    println!("Part 1: {}", part_1(&tups));
    println!("Part 2: {}", part_2(&tups));
}
