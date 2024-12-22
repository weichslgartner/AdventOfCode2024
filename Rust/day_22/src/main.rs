use rayon::iter::IntoParallelRefIterator;
use rayon::iter::ParallelIterator;
use std::collections::HashMap;

const PATTERN_LENGTH: usize = 4;

fn parse_input(input: &str) -> Vec<i64> {
    input
        .lines()
        .filter_map(|line| line.parse::<i64>().ok())
        .collect()
}

fn calc_secret_numbers(mut secret_number: i64, rounds: usize) -> (i64, Vec<i64>) {
    let mut prices = Vec::new();

    for _ in 0..rounds {
        prices.push(secret_number % 10);
        secret_number = secret_number ^ ((secret_number * 64) % 16_777_216);
        secret_number = secret_number ^ (secret_number / 32);
        secret_number = secret_number ^ ((secret_number * 2048) % 16_777_216);
    }

    (secret_number, prices)
}

fn calc_price_for_pattern(prices: &[i64]) -> HashMap<Vec<i64>, i64> {
    let diffs: Vec<i64> = prices.windows(2).map(|pair| pair[1] - pair[0]).collect();
    let mut pattern_dict = HashMap::new();

    for i in 0..(diffs.len() - PATTERN_LENGTH) {
        let pattern: Vec<i64> = diffs[i..i + PATTERN_LENGTH].to_vec();
        let price = prices[i + PATTERN_LENGTH];
        pattern_dict.entry(pattern).or_insert(price);
    }

    pattern_dict
}

fn part_1(secrets: &[i64]) -> i64 {
    secrets.iter().sum()
}

fn merge_maps(
    mut map1: HashMap<Vec<i64>, i64>,
    map2: HashMap<Vec<i64>, i64>,
) -> HashMap<Vec<i64>, i64> {
    for (key, value) in map2 {
        *map1.entry(key).or_insert(0) += value;
    }
    map1
}
fn part_2(prices_list: &[Vec<i64>]) -> i64 {
    *prices_list
        .par_iter()
        .map(|prices| calc_price_for_pattern(prices))
        .fold_with(HashMap::new(), merge_maps)
        .reduce(HashMap::new, merge_maps)
        .values()
        .max()
        .unwrap()
}

fn main() {
    let input = include_str!("../../../inputs/input_22.txt");

    let numbers = parse_input(input);
    let secrets: Vec<(i64, Vec<i64>)> = numbers
        .iter()
        .map(|&n| calc_secret_numbers(n, 2000))
        .collect();

    let part_1_result = part_1(
        &secrets
            .iter()
            .map(|(secret, _)| *secret)
            .collect::<Vec<_>>(),
    );
    let part_2_result = part_2(
        &secrets
            .iter()
            .map(|(_, prices)| prices.clone())
            .collect::<Vec<_>>(),
    );

    println!("Part 1: {}", part_1_result);
    println!("Part 2: {}", part_2_result);
}
