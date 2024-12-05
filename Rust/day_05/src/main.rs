use std::{
    cmp::Ordering,
    collections::{HashMap, HashSet},
};

fn parse_input(input: &str) -> (HashMap<i32, HashSet<i32>>, Vec<Vec<i32>>) {
    let mut sections = input.split("\n\n");
    let rules_section = sections.next().unwrap();
    let pages_section = sections.next().unwrap();

    let mut rules = HashMap::new();
    for line in rules_section.lines() {
        let nums: Vec<i32> = line
            .split("|")
            .filter_map(|x| x.parse::<i32>().ok())
            .collect();
        if nums.len() == 2 {
            rules
                .entry(nums[0])
                .or_insert_with(HashSet::new)
                .insert(nums[1]);
        }
    }

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
    for i in (0..update.len()).rev() {
        let p = update[i];
        let rest: HashSet<i32> = update[..i].iter().cloned().collect();
        if let Some(required) = rules.get(&p) {
            if !rest.is_disjoint(required) {
                return false;
            }
        }
    }
    true
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
    let (rules, mut pages) = parse_input(&input);
    println!("Part 1: {}", part_1(&rules, &pages));
    println!("Part 2: {}", part_2(&rules, &mut pages));
}
