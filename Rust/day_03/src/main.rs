use regex::Regex;

type Tuple = (String, String, String, i32, i32);

fn parse_input(line: &str) -> Vec<Tuple> {
    let re = Regex::new(r"(do\(\))|(don't\(\))|(mul\((\d+),(\d+)\))").unwrap();
    re.captures_iter(line)
        .map(|cap| {
            let do_group = cap.get(1).map_or("", |m| m.as_str()).to_string();
            let dont_group = cap.get(2).map_or("", |m| m.as_str()).to_string();
            let mul_group = cap.get(3).map_or("", |m| m.as_str()).to_string();
            let first_num = cap.get(4).map_or("0", |m| m.as_str()).parse::<i32>().unwrap_or(0);
            let second_num = cap.get(5).map_or("0", |m| m.as_str()).parse::<i32>().unwrap_or(0);
            (do_group, dont_group, mul_group, first_num, second_num)
        })
        .collect()
}

fn part_1(tups: &[Tuple]) -> i32 {
    tups.iter()
        .filter(|tup| !tup.2.is_empty())
        .map(|tup| tup.3 * tup.4)
        .sum()
}

fn conditional_mul(state: (bool, i32), el: &Tuple) -> (bool, i32) {
    let (mut enabled, mut total) = state;
    if el.0 == "do()" {
        enabled = true;
    } else if el.1 == "don't()" {
        enabled = false;
    } else if el.2.starts_with("mul") && enabled {
        total += el.3 * el.4;
    }
    (enabled, total)
}

fn part_2(tups: &[Tuple]) -> i32 {
    tups.iter().fold((true, 0), conditional_mul).1
}

fn main() {
    let line = include_str!("../../../inputs/input_03.txt");
    let tups = parse_input(line);
    println!("Part 1: {}", part_1(&tups));
    println!("Part 2: {}", part_2(&tups));
}

