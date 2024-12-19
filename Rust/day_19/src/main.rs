use cached::proc_macro::cached;

fn parse_input(input: &str) -> (Vec<String>, Vec<String>) {
    let parts: Vec<&str> = input.split("\n\n").collect();
    let towels = parts[0]
        .split(',')
        .map(|t| t.trim().to_string())
        .collect();
    let patterns = parts[1]
        .lines()
        .map(|p| p.to_string())
        .collect();
    (towels, patterns)
}

#[cached]
fn cnt_valid_designs(towels: Vec<String>, pattern: String) -> usize {
    if pattern.is_empty() {
        return 1;
    }

    towels
        .iter()
        .filter(|t| pattern.starts_with(t.as_str()))
        .map(|t| {
            let remaining_pattern = pattern[t.len()..].to_string();
            cnt_valid_designs(towels.clone(), remaining_pattern)
        })
        .sum()
}

fn part_1(towels: Vec<String>, patterns: Vec<String>) -> usize {
    patterns
        .iter()
        .map(|p| cnt_valid_designs(towels.clone(), p.clone()) > 0)
        .filter(|&valid| valid)
        .count() 
}

fn part_2(towels: Vec<String>, patterns: Vec<String>) -> usize {
    patterns
        .iter()
        .map(|p| cnt_valid_designs(towels.clone(), p.clone()))
        .sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_19.txt");
    let (towels, patterns) = parse_input(input);
    println!("Part 1: {}", part_1(towels.clone(), patterns.clone()));
    println!("Part 2: {}", part_2(towels, patterns));
}



