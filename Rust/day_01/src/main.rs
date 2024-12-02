use anyhow::{Context, Result};
use itertools::Itertools;

fn parse_input(input: &str) -> Result<(Vec<i64>, Vec<i64>)> {
    input
        .lines()
        .map(|line| {
            aoc::line_to_int::<i64, ' '>(line)?                
                .into_iter()
                .collect_tuple()
                .context("Failed to convert line to tuple")
        })
        .collect::<Result<Vec<(i64, i64)>>>()
        .map(|pairs| pairs.into_iter().unzip())
}

fn part_1(l1: &[i64], l2: &[i64]) -> i64 {
    l1.iter()
        .sorted()
        .zip(l2.iter().sorted())
        .map(|(a, b)| (a - b).abs())
        .sum()
}

fn part_2(l1: &[i64], l2: &[i64]) -> i64 {
    let count = l2.iter().counts();
    l1.iter()
        .map(|x| x * (*count.get(x).unwrap_or(&0) as i64))
        .sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_01.txt");
    let (l1, l2) = parse_input(input).unwrap();
    println!("Part 1: {}", part_1(&l1, &l2));
    println!("Part 2: {}", part_2(&l1, &l2));
}
