use std::collections::{HashMap, HashSet};

// Parse input into rules and pages
fn parse_input(input: &str) -> (HashMap<i32, HashSet<i32>>, Vec<Vec<i32>>) {
    let mut sections = input.split("\n\n");
    let rules_section = sections.next().unwrap();
    let pages_section = sections.next().unwrap();
    
    let mut rules = HashMap::new();
    for line in rules_section.lines() {
        let nums: Vec<i32> = line.split("")
            .filter_map(|x| x.parse::<i32>().ok())
            .collect();
        if nums.len() == 2 {
            rules.entry(nums[0])
                .or_insert_with(HashSet::new)
                .insert(nums[1]);
        }
    }

    let pages = pages_section.lines()
        .map(|line| line.split("|")
            .filter_map(|x| x.parse::<i32>().ok())
            .collect())
        .collect();
    
    (rules, pages)
}

// Check if an update is in order based on the rules
fn is_in_order(update: &Vec<i32>, rules: &HashMap<i32, HashSet<i32>>) -> bool {
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

// Recursive function to fix an unordered update
fn fix(cur: Vec<i32>, rest: Vec<i32>, rules: &HashMap<i32, HashSet<i32>>) -> Option<Vec<i32>> {
    if rest.is_empty() && is_in_order(&cur, rules) {
        return Some(cur);
    }

    for i in 0..rest.len() {
        let mut next_cur = cur.clone();
        next_cur.push(rest[i]);
        
        if is_in_order(&next_cur, rules) {
            let mut next_rest = rest.clone();
            next_rest.remove(i);
            
            if let Some(result) = fix(next_cur, next_rest, rules) {
                return Some(result);
            }
        }
    }

    None
}




fn part_1(rules: &HashMap<i32, HashSet<i32>>, pages: &Vec<Vec<i32>>) -> i32 {
    pages.iter()
        .filter(|update| is_in_order(update, rules))
        .map(|update| update[update.len() / 2])
        .sum()
}

fn part_2(rules: &HashMap<i32, HashSet<i32>>, pages: &Vec<Vec<i32>>) -> i32 {
    pages.iter()
        .filter_map(|update| {
            if !is_in_order(update, rules) {
                fix(vec![], update.clone(), rules)
                    .map(|fixed| fixed[fixed.len() / 2])
            }else{
                None
            }
        })
        .sum()
}


fn main() {
    let input = include_str!("../../../inputs/input_05.txt");
    let (rules, pages) = parse_input(&input);
    println!("Part 1: {}", part_1(&rules, &pages));
    println!("Part 2: {}",  part_2(&rules, &pages));
}

