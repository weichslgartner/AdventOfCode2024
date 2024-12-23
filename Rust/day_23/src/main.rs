use std::collections::{HashMap, HashSet};

type Connections = HashMap<String, Vec<String>>;

fn  parse_input(input: &str) -> Connections {
    let mut connections: Connections = HashMap::new();
    for line in input.lines() {
        let parts: Vec<&str> = line.split('-').collect();
        let src = parts[0].to_string();
        let dst = parts[1].to_string();

        connections.entry(src.clone()).or_default().push(dst.clone());
        connections.entry(dst).or_default().push(src);
    }
    connections
}

fn get_three_way_cliques(connections: &Connections) -> HashSet<String> {
    let mut three_way = HashSet::new();
    for (src, dsts) in connections {
        for dst in dsts {
            if let Some(candidates) = connections.get(dst) {
                for c in candidates {
                    if dsts.contains(c) {
                        let mut group = [src.clone(), dst.clone(), c.clone()];
                        group.sort();
                        three_way.insert(group.join(","));
                    }
                }
            }
        }
    }
    three_way
}

fn can_add(group: &[String], candidate: &str, connections: &Connections) -> bool {
    group.iter().all(|g| connections.get(g).map_or(false, |neighbors| neighbors.contains(&candidate.to_string())))
}

fn part_1(three_way: &HashSet<String>) -> usize {
    three_way.iter().filter(|node| {
        node.split(',').any(|n| n.starts_with('t'))
    }).count()
}

fn part_2(three_way: &HashSet<String>, connections: &Connections) -> String {
    let mut biggest_group: Vec<String> = Vec::new();
    for group_str in three_way {
        let mut group: Vec<String> = group_str.split(',').map(|s| s.to_string()).collect();
        if let Some(candidates) = connections.get(&group[0]) {
            for candidate in candidates.iter() {
                if !group.contains(candidate) && can_add(&group[1..], candidate, connections) {
                    group.push(candidate.clone());
                    if group.len() > biggest_group.len() {
                        biggest_group = group.clone();
                    }
                }
            }
        }
    }
    biggest_group.sort();
    biggest_group.join(",")
}

fn main() {
    let input = include_str!("../../../inputs/input_23.txt");
    let connections = parse_input(input);
    let three_way = get_three_way_cliques(&connections);
    println!("Part 1: {}", part_1(&three_way));
    println!("Part 2: {}", part_2(&three_way, &connections));
}


