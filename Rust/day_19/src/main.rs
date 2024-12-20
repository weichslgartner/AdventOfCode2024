use cached::proc_macro::cached;
use lazy_static::lazy_static;
use std::sync::RwLock;

lazy_static! {
    static ref TOWELS: RwLock<Vec<&'static str>> = RwLock::new(Vec::new());
}

fn parse_input(input: &str) -> Vec<String> {
    let (towelz, patternz) = input.split_once("\n\n").unwrap();
    let patterns = patternz.lines().map(|p| p.to_string()).collect();
    let towels: Vec<&'static str> = towelz
        .split(',')
        .map(|t| Box::leak(t.trim().to_string().into_boxed_str()) as &'static str) // Cast to immutable reference
        .collect();

    {
        let mut towels_global = TOWELS.write().unwrap();
        *towels_global = towels;
    }
    patterns
}

#[cached]
fn cnt_valid_designs(pattern: String) -> usize {
    if pattern.is_empty() {
        return 1;
    }
    TOWELS.read().unwrap()
        .iter()
        .filter(|t| pattern.starts_with(*t))
        .map(|t| {
            cnt_valid_designs(pattern[t.len()..].to_string())
        })
        .sum()
}

fn part_1(patterns: &[String]) -> usize {
    patterns
        .iter()
        .map(|p| cnt_valid_designs( p.clone()) > 0)
        .filter(|&valid| valid)
        .count()
}

fn part_2(patterns: &[String]) -> usize {
    patterns
        .iter()
        .map(|p| cnt_valid_designs(p.clone()))
        .sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_19.txt");
    let patterns = parse_input(input);
    println!("Part 1: {}", part_1(&patterns));
    println!("Part 2: {}", part_2(&patterns));
}
