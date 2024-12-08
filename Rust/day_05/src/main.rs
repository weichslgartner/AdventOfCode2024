use std::{
    cmp::Ordering,
    collections::{HashMap, HashSet},
};

fn parse_input(input: &str) -> (HashMap<i32, HashSet<i32>>, Vec<Vec<i32>>) {
    let (rules_section, pages_section) = input.split_once("\n\n").unwrap();
    let rules = rules_section
        .lines()
        .map(|line| {
            line.split("|")
                .filter_map(|x| x.parse::<i32>().ok())
                .collect::<Vec<_>>()
        })
        .fold(
            HashMap::new(),
            |mut acc: HashMap<i32, HashSet<i32>>, nums| {
                if nums.len() > 1 {
                    acc.entry(nums[0]).or_default().insert(nums[1]);
                }
                acc
            },
        );
    let pages = pages_section
        .lines()
        .map(|line| {
            line.split(",")
                .filter_map(|x| x.parse::<i32>().ok())
                .collect()
        })
        .collect();

    (rules, pages)
}

fn is_in_order(update: &[i32], rules: &HashMap<i32, HashSet<i32>>) -> bool {
    (0..update.len()).rev().all(|i| {
        rules
            .get(&update[i])
            .unwrap()
            .is_disjoint(&update[..i].iter().cloned().collect::<HashSet<i32>>())
    })
}

fn part_1(rules: &HashMap<i32, HashSet<i32>>, pages: &[Vec<i32>]) -> i32 {
    pages
        .iter()
        .filter(|update| is_in_order(update, rules))
        .map(|update| update[update.len() / 2])
        .sum()
}

fn part_2(rules: &HashMap<i32, HashSet<i32>>, pages: &mut [Vec<i32>]) -> i32 {
    pages
        .iter_mut()
        .filter(|page| !is_in_order(page, rules))
        .map(|page| {
            let l = page.len() / 2;
            let (_, median, _) = page.select_nth_unstable_by(l, |a, b| {
                if rules.get(a).map_or(false, |set| set.contains(b)) {
                    Ordering::Less
                } else {
                    Ordering::Greater
                }
            });
            *median
        })
        .sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_05.txt");
    let (rules, mut pages) = parse_input(input);
    println!("Part 1: {}", part_1(&rules, &pages));
    println!("Part 2: {}", part_2(&rules, &mut pages));
}
